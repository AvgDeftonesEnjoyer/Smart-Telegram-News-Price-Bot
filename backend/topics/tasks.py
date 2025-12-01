from celery import shared_task
from django.utils import timezone

from news_providers.crypto import get_crypto_trending
from topics.models import Topic, FeedItem
from subscriptions.models import Subscription
from telegram import Bot
from smart_bot.settings import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

@shared_task
def fetch_crypto_news_task():
    data = get_crypto_trending()
    topic = Topic.objects.get(name='crypto')

    FeedItem.objects.create(
        topic=topic,
        title='Crypto Trending Update',
        url='https://coingecko.com/en',
        source='coingecko'
    )

    return "Crypto feed updated"

@shared_task
def send_topic_updates_task():

    subscriptions = Subscription.objects.select_related('user', 'topic')

    for sub in subscriptions:
        topic=sub.topic
        user=sub.user
        feed_items = FeedItem.objects.filter(topic=topic).order_by('-created_at')[:1]

        if feed_items:
            item = feed_items[0]
            text = f"📰 *{topic.name} Update*\n\n{item.title}\n\n{item.url}"

            try:
                bot.send_message(
                    chat_id=user.telegram_id,
                    text=text,
                    parse_mode='Markdown'
                )
            except Exception as e:
                print(f"Error sending message to {user.telegram_id}: {e}")

    return "Broadcast completed"

    