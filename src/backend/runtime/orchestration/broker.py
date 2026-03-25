from core.settings import get_settings
from taskiq_redis import RedisStreamBroker

settings = get_settings()

DEFAULT_TASKIQ_QUEUE_NAME = "registries:taskiq"
DEFAULT_TASKIQ_CONSUMER_GROUP = "registries:backend"

broker = RedisStreamBroker(
    url=settings.redis_url,
    queue_name=DEFAULT_TASKIQ_QUEUE_NAME,
    consumer_group_name=DEFAULT_TASKIQ_CONSUMER_GROUP,
)
