from typing import Optional
import redis.asyncio as redis
from app.settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

redis_client = None

def init_redis():
    global redis_client
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        decode_responses=True
    )
    return redis_client

async def set_redis_key(key: str, value: str, ex: int = 3600):
    """Set a key in Redis with optional expiry (default 1 hour)"""
    await redis_client.set(key, value, ex=ex)

async def get_redis_key(key: str) -> Optional[str]:
    """Get a value from Redis by key"""
    return await redis_client.get(key)

async def delete_redis_key(key: str):
    """Delete a key from Redis"""
    await redis_client.delete(key)