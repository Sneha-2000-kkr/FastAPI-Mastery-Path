import asyncio
import random


async def fetch_quote(symbol: str) -> dict:
    """Fake upstream with 300ms latency."""
    await asyncio.sleep(0.3)
    return {
        "symbol": symbol.upper(),
        "price": round(random.uniform(10, 500), 2),
        "currency": "USD",
    }
