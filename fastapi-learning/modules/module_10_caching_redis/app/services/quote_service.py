import asyncio
import json

from redis.asyncio import Redis

from app.core.config import get_settings
from app.services.external_quote import fetch_quote


def _key(symbol: str) -> str:
    return f"{get_settings().cache_namespace}:quotes:{symbol.upper()}"


def _lock_key(symbol: str) -> str:
    return _key(symbol) + ":lock"


class QuoteService:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        self.ttl = get_settings().cache_ttl_seconds

    async def get(self, symbol: str) -> dict:
        cached = await self.redis.get(_key(symbol))
        if cached is not None:
            return {"data": json.loads(cached), "source": "cache"}

        # Single-flight via SET NX. The first caller refreshes; others wait briefly.
        got_lock = await self.redis.set(_lock_key(symbol), "1", nx=True, ex=10)
        if not got_lock:
            for _ in range(20):
                await asyncio.sleep(0.05)
                cached = await self.redis.get(_key(symbol))
                if cached is not None:
                    return {"data": json.loads(cached), "source": "cache"}
            # fall through and refetch ourselves

        try:
            data = await fetch_quote(symbol)
            await self.redis.set(_key(symbol), json.dumps(data), ex=self.ttl)
            return {"data": data, "source": "origin"}
        finally:
            await self.redis.delete(_lock_key(symbol))

    async def invalidate(self, symbol: str) -> int:
        return await self.redis.delete(_key(symbol))
