from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from asgiref.sync import sync_to_async

from users.models import CustomUser
from subscriptions.models import Subscription
from bot.default_topics import DEFAULT_TOPICS
from news_providers.crypto import get_crypto_trending

#Response on command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your Smart Bot.")

#Response on command /subscribe
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user, created = await sync_to_async(CustomUser.objects.get_or_create)(
        telegram_id=update.effective_user.id,
        defaults={
            'username': update.effective_user.username
        }
    )
    await update.message.reply_text(f'Here are default topics: {DEFAULT_TOPICS}')
    if context.args:
        topic = ' '.join(context.args)
        await sync_to_async(Subscription.objects.create)(user=user, topic=topic)
        await update.message.reply_text(f'Successfully subscribed to {topic}')
    else:
        await update.message.reply_text('Please provide a topic to subscribe to.')
    
#Response on command /unsubscribe
async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = await sync_to_async(CustomUser.objects.get)(telegram_id=update.effective_user.id)
    except CustomUser.DoesNotExist:
        await update.message.reply_text('You are not subscribed to any topics.')
        return
    
    user_topics = Subscription.objects.filter(user=user)

    if context.args:
        topic = ' '.join(context.args)
        user_topic = await sync_to_async(user_topics.filter(topic=topic).first)()

        if user_topic:
            await sync_to_async(user_topic.delete)()
            await update.message.reply_text(f'Successfully unsubscribed from {topic}')
        else:
            await update.message.reply_text(f'You are not subscribed to {topic}')
            
async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        trending = get_crypto_trending()
        text = '\n\n'.join(trending)
        await update.message.reply_text(text, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Error fetching crypto trending: {e}")