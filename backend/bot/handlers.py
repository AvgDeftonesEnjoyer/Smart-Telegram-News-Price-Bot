from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from asgiref.sync import sync_to_async
import logging

from users.models import CustomUser
from subscriptions.models import Subscription
from topics.models import Topic
from bot.default_topics import DEFAULT_TOPICS
from news_providers.crypto import get_crypto_trending

# Configure logging
logger = logging.getLogger(__name__)

# Helper function to get or create user (DRY principle)
async def get_user(telegram_id, username):
    """Get or create user by telegram_id and username."""
    try:
        user, created = await sync_to_async(CustomUser.objects.get_or_create)(
            telegram_id=telegram_id,
            defaults={'username': username}
        )
        if created:
            logger.info(f"New user created: {telegram_id} (@{username})")
        return user, created
    except Exception as e:
        logger.error(f"Error getting/creating user {telegram_id}: {e}")
        raise

#Response on command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        telegram_id = update.effective_user.id
        username = update.effective_user.username
        
        user, created = await get_user(telegram_id, username)

        if created:
            await update.message.reply_text("Welcome to Smart Bot! You have been successfully registered.")
            logger.info(f"User {telegram_id} registered via /start")
        else:
            await update.message.reply_text("Welcome back to Smart Bot!")
            logger.info(f"User {telegram_id} returned via /start")
    except Exception as e:
        logger.error(f"Error in /start command: {e}", exc_info=True)
        await update.message.reply_text("Sorry, an error occurred. Please try again later.")

#Response on command /subscribe
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        telegram_id = update.effective_user.id
        username = update.effective_user.username

        user, created = await get_user(telegram_id, username)

        if not context.args:
            await update.message.reply_text("Please specify a topic to subscribe. Example: /subscribe crypto")
            return

        topic_name = " ".join(context.args)

        try:
            topic = await sync_to_async(Topic.objects.get)(name=topic_name)
        except Topic.DoesNotExist:
            logger.warning(f"User {telegram_id} tried to subscribe to non-existent topic: {topic_name}")
            await update.message.reply_text(f"Topic '{topic_name}' does not exist.")
            return

        # Check if subscription already exists
        exists = await sync_to_async(
            lambda: Subscription.objects.filter(user=user, topic=topic).exists()
        )()
        if exists:
            await update.message.reply_text(f"You are already subscribed to {topic.name}")
            return

        await sync_to_async(Subscription.objects.create)(user=user, topic=topic)
        await update.message.reply_text(f"Successfully subscribed to {topic.name}")
        logger.info(f"User {telegram_id} subscribed to topic: {topic.name}")
    except Exception as e:
        logger.error(f"Error in /subscribe command for user {update.effective_user.id}: {e}", exc_info=True)
        await update.message.reply_text("Sorry, an error occurred while subscribing. Please try again later.")

#Response on command /unsubscribe
async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        telegram_id = update.effective_user.id
        username = update.effective_user.username

        user, created = await get_user(telegram_id, username)

        if not context.args:
            await update.message.reply_text("Specify topic to unsubscribe. Example: /unsubscribe crypto")
            return

        topic_name = ' '.join(context.args).lower()
        try:
            topic = await sync_to_async(Topic.objects.get)(name=topic_name)
        except Topic.DoesNotExist:
            logger.warning(f"User {telegram_id} tried to unsubscribe from non-existent topic: {topic_name}")
            await update.message.reply_text(f"Topic '{topic_name}' does not exist.")
            return

        sub = await sync_to_async(Subscription.objects.filter(user=user, topic=topic).first)()
        if not sub:
            await update.message.reply_text(f"You are not subscribed to '{topic_name}'.")
            return

        await sync_to_async(sub.delete)()
        await update.message.reply_text(f"Unsubscribed from '{topic_name}'.")
        logger.info(f"User {telegram_id} unsubscribed from topic: {topic_name}")
    except Exception as e:
        logger.error(f"Error in /unsubscribe command for user {update.effective_user.id}: {e}", exc_info=True)
        await update.message.reply_text("Sorry, an error occurred while unsubscribing. Please try again later.")

#Response on command /crypto
async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.info(f"User {update.effective_user.id} requested /crypto")
        trending = get_crypto_trending()
        if not trending:
            await update.message.reply_text("No crypto data available at the moment. Please try again later.")
            return
        text = '\n\n'.join(trending)
        await update.message.reply_text(text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in /crypto command: {e}", exc_info=True)
        await update.message.reply_text("Sorry, an error occurred while fetching crypto data. Please try again later.")

#Response on command /mytopics
async def mytopics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        telegram_id = update.effective_user.id
        username = update.effective_user.username

        user, created = await get_user(telegram_id, username)
        
        user_topics = await sync_to_async(list)(
            Subscription.objects.filter(user=user).select_related('topic')
        )

        if not user_topics:
            await update.message.reply_text("You are not subscribed to any topics.")
            return

        topics_text = "\n".join(
            [f"- {sub.topic.name}" for sub in user_topics]
        )

        await update.message.reply_text(
            f"Your subscriptions:\n\n{topics_text}"
        )
        logger.info(f"User {telegram_id} viewed their topics")
    except Exception as e:
        logger.error(f"Error in /mytopics command for user {update.effective_user.id}: {e}", exc_info=True)
        await update.message.reply_text("Sorry, an error occurred while fetching your topics. Please try again later.")