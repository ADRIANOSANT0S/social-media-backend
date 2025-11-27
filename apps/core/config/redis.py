"""
r: This module defines the base Redis settings.

Args:
    host: Host of the Redis server.
    port: Port of the Redis server.
    db: The Redis database number (0-14).

Reference:
    For more information, visit: https://redis.io/topics/quickstart
"""

from django.conf import settings
from redis import Redis

r = Redis(
    host=getattr(settings, "REDIS_HOST", "localhost"),
    port=getattr(settings, "REDIS_PORT", 6379),
    db=getattr(settings, "REDIS_DB", 0),
)
