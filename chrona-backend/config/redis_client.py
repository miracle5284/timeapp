import redis.asyncio as async_redis
from django.conf import settings

redis_client = async_redis.Redis(
    host= settings.REDIS_HOST,
    port= settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
    ssl=True
)
