from core.settings import get_settings
from taskiq_redis import RedisStreamBroker

# Broker bootstrap is runtime-owned and intentionally module-scoped. Importers
# consume the shared broker instance instead of building competing brokers.
settings = get_settings()

broker = RedisStreamBroker(
    url=settings.db.redis_url,
    queue_name=settings.broker.taskiq_queue_name,
    consumer_group_name=settings.broker.taskiq_consumer_group_name,
)
