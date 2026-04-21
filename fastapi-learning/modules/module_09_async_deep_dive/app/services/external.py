import asyncio
import random


async def fetch_profile(uid: int) -> dict:
    await asyncio.sleep(random.uniform(0.1, 0.4))
    return {"uid": uid, "name": f"User {uid}"}


async def fetch_orders(uid: int) -> list[dict]:
    await asyncio.sleep(random.uniform(0.1, 0.4))
    return [{"id": i, "uid": uid} for i in range(3)]


async def fetch_recommendations(uid: int) -> list[str]:
    await asyncio.sleep(random.uniform(0.1, 0.4))
    return [f"item-{i}" for i in range(5)]
