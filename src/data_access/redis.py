from redis.asyncio import ConnectionPool as AsyncConnectionPool
from redis.asyncio import Redis

from config import settings


base_redis_config = dict(
    host=settings.redis_host,
    port=int(settings.redis_port),
    username=settings.redis_user,
    password=settings.redis_password
)

async_redis_pool = AsyncConnectionPool(
    **base_redis_config,
    db=2,
    max_connections=300,
)

async_redis_client = Redis(
    ssl=False,
    single_connection_client=False,
    connection_pool=async_redis_pool,
    max_connections=None,
    decode_responses=True
)
