from redis.asyncio import Redis, from_url

from app.core.config import get_settings

_client: Redis | None = None


async def init() -> Redis:
    global _client
    _client = from_url(get_settings().redis_url, decode_responses=True)
    await _client.ping()
    return _client


async def close() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


def get_redis() -> Redis:
    if _client is None:
        raise RuntimeError("Redis not initialised")
    return _client
