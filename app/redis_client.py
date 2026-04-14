import redis
import json
from typing import Optional
from .config import settings

# Create Redis connection
redis_client = redis.Redis(
    host=getattr(settings, 'redis_host', 'localhost'),
    port=getattr(settings, 'redis_port', 6379),
    decode_responses=True
)


def get_cache(key: str) -> Optional[dict]:
    """Get cached data from Redis"""
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"Redis get error: {e}")
        return None


def set_cache(key: str, value: dict, expire: int = 300):
    """Set cache in Redis with expiration (default 5 minutes)"""
    try:
        redis_client.setex(key, expire, json.dumps(value))
    except Exception as e:
        print(f"Redis set error: {e}")


def delete_cache(pattern: str):
    """Delete cache keys matching pattern"""
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except Exception as e:
        print(f"Redis delete error: {e}")
