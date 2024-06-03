import aioredis
from aioredis.client import Redis

from src.settings import settings

REDIS_URL: str = f"redis://{settings.REDIS_SERVER}:{settings.REDIS_PORT}"

client: Redis = aioredis.from_url(REDIS_URL)


async def redis_set(key: int, data: int) -> None:
    await client.set(str(key), data, ex=settings.CACHE_LIFETIME)
    return


async def redis_get(key: int) -> int | None:
    data = await client.get(str(key))
    if not data:
        return None
    return data
