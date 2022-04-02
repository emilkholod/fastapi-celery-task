import os

import redis

redis_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
redis_app = redis.Redis.from_url(redis_url)
