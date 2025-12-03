from celery import shared_task
from django.utils import timezone
import asyncio
import logging

from news_providers.crypto import get_crypto_trending
from topics.models import Topic, FeedItem
from subscriptions.models import Subscription
from telegram import Bot
from smart_bot.settings import BOT_TOKEN

logger = logging.getLogger(__name__)

@shared_task
def fetch_crypto_news_task():
    """Fetch crypto trending data and save to database."""
    try:
        logger.info("Starting crypto news fetch task")
        # Get crypto trending data
        data = get_crypto_trending()
        
        # Get or create crypto topic
        topic, created = Topic.objects.get_or_create(name='crypto')
        
        # Create feed item with actual data
        if data:
            # Join all trending items into one message
            content = '\n\n'.join(data)
            FeedItem.objects.create(
                topic=topic,
                title='Crypto Trending Update',
                content=content,
                url='https://coingecko.com/en',
                source='coingecko'
            )
            logger.info(f"Crypto feed updated with {len(data)} items")
            return f"Crypto feed updated with {len(data)} items"
        else:
            logger.warning("No crypto data available")
            return "No crypto data available"
    except Exception as e:
        logger.error(f"Error fetching crypto news: {str(e)}", exc_info=True)
        return f"Error fetching crypto news: {str(e)}"

@shared_task
def send_topic_updates_task():
    """Send topic updates to all subscribed users."""
    try:
        logger.info("Starting topic updates broadcast task")
        bot = Bot(token=BOT_TOKEN)
        
        subscriptions = Subscription.objects.select_related('user', 'topic')
        sent_count = 0
        error_count = 0

        for sub in subscriptions:
            topic = sub.topic
            user = sub.user
            
            # Get latest feed item for this topic
            feed_item = FeedItem.objects.filter(topic=topic).order_by('-created_at').first()

            if feed_item:
                # Build message text
                text = f"📰 *{topic.name.capitalize()} Update*\n\n"
                text += f"{feed_item.title}\n\n"
                
                # Add content if available
                if hasattr(feed_item, 'content') and feed_item.content:
                    text += f"{feed_item.content}\n\n"
                
                text += f"🔗 {feed_item.url}"

                try:
                    # Run async send_message in sync context
                    asyncio.run(
                        bot.send_message(
                            chat_id=user.telegram_id,
                            text=text,
                            parse_mode='Markdown'
                        )
                    )
                    sent_count += 1
                    logger.debug(f"Sent update to user {user.telegram_id}")
                except Exception as e:
                    error_count += 1
                    logger.error(f"Error sending message to {user.telegram_id}: {e}")

        result = f"Broadcast completed: {sent_count} sent, {error_count} errors"
        logger.info(result)
        return result
    except Exception as e:
        logger.error(f"Error in send_topic_updates_task: {str(e)}", exc_info=True)
        return f"Error in broadcast task: {str(e)}"