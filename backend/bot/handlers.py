from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from asgiref.sync import sync_to_async

from users.models import CustomUser
from subscriptions.models import Subscription
from bot.default_topics import DEFAULT_TOPICS
from news_providers.crypto import get_crypto_trending

#Response on command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    username = update.effective_user.username
    
    user, created = await sync_to_async(CustomUser.objects.get_or_create)(
        telegram_id=telegram_id,
        defaults={
            'username': username
        }
    )

    if created:
        await update.message.reply_text("Welcome to Smart Bot! You have been successfully registered.")
    else:
        await update.message.reply_text("Welcome back to Smart Bot!")

#Response on command /subscribe
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user, created = await sync_to_async(CustomUser.objects.get_or_create)(
        telegram_id=update.effective_user.id,
        defaults={
            'username': update.effective_user.username
        }
    )
    await update.message.reply_text(f'Here are default topics: {DEFAULT_TOPICS}')
    if not context.args:
        topics = await sync_to_async(list)(Topic.objects.all())
        topic_list = "\n".join([f"- {t.name}" for t in topics])

        await update.message.reply_text(
            "Available topics:\n" + topic_list +
            "\n\nUse: /subscribe <topic>"
        )
        return

    topic_name = " ".join(context.args)

    try:
        topic = await sync_to_async(Topic.objects.get)(name=topic_name)
    except Topic.DoesNotExist:
        await update.message.reply_text(f"Topic '{topic_name}' does not exist.")
        return
    
    subscription, created = await sync_to_async(Subscription.objects.get_or_create)(
        user=user,
        topic=topic
    )
    
    try:
        await sync_to_async(Subscription.objects.create)(user=user, topic=topic)
        await update.message.reply_text(f"Successfully subscribed to *{topic.name}*")
    except:
        await update.message.reply_text(f"You are already subscribed to *{topic.name}*")
    
#Response on command /unsubscribe
async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    try:
        user = await sync_to_async(CustomUser.objects.get)(telegram_id=telegram_id)
    except CustomUser.DoesNotExist:
        await update.message.reply_text("You are not registered.")
        return

    if not context.args:
        user_topics = await sync_to_async(list)(
            Subscription.objects.filter(user=user).select_related("topic")
        )

        if not user_topics:
            await update.message.reply_text("You are not subscribed to any topics.")
            return

        topics_list = "\n".join([f"- {sub.topic.name}" for sub in user_topics])
        await update.message.reply_text(
            "Your subscriptions:\n" + topics_list +
            "\n\nUse: /unsubscribe <topic>"
        )
        return

    topic_name = " ".join(context.args)

    try:
        topic = await sync_to_async(Topic.objects.get)(name__iexact=topic_name)
    except Topic.DoesNotExist:
        await update.message.reply_text(f"No such topic: {topic_name}")
        return

    sub = await sync_to_async(Subscription.objects.filter(user=user, topic=topic).first)()
    if sub:
        await sync_to_async(sub.delete)()
        await update.message.reply_text(f"Unsubscribed from {topic.name}")
    else:
        await update.message.reply_text(f"You are not subscribed to {topic.name}")

#Response on command /crypto
async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        trending = get_crypto_trending()
        text = '\n\n'.join(trending)
        await update.message.reply_text(text, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Error fetching crypto trending: {e}")

#Response on command /mytopics
async def mytopics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    try:
        user = await sync_to_async(CustomUser.objects.get)(telegram_id = telegram_id)
    except CustomUser.DoesNotExist:
        await update.message.reply_text("You are not registered.")
        return
    
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