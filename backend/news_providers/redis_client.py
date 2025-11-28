import redis
from django.conf import settings

redis_config = {
    'host': settings.REDIS_HOST,
    'port': settings.REDIS_PORT,
    'db': settings.REDIS_DB,
    'decode_responses': True
}

# Додаємо password тільки якщо він встановлений
if settings.REDIS_PASSWORD:
    redis_config['password'] = settings.REDIS_PASSWORD

r = redis.Redis(**redis_config)