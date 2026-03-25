from core.settings import get_settings
from taskiq_redis import RedisStreamBroker

settings = get_settings()

broker = RedisStreamBroker(
    url=settings.db.redis_url,
    queue_name=settings.broker.taskiq_queue_name,
    consumer_group_name=settings.broker.taskiq_consumer_group_name,
)
