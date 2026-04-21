import asyncio
import time

from fastapi import APIRouter

from app.services.external import fetch_orders, fetch_profile, fetch_recommendations

router = APIRouter(tags=["async"])


@router.get("/fanout")
async def fanout(uid: int = 1) -> dict:
    t0 = time.perf_counter()
    profile, orders, recs = await asyncio.gather(
        fetch_profile(uid),
        fetch_orders(uid),
        fetch_recommendations(uid),
    )
    return {"profile": profile, "orders": orders, "recs": recs,
            "ms": int((time.perf_counter() - t0) * 1000)}


@router.get("/fanout-tg")
async def fanout_tg(uid: int = 1) -> dict:
    t0 = time.perf_counter()
    async with asyncio.TaskGroup() as tg:
        p = tg.create_task(fetch_profile(uid))
        o = tg.create_task(fetch_orders(uid))
        r = tg.create_task(fetch_recommendations(uid))
    return {"profile": p.result(), "orders": o.result(), "recs": r.result(),
            "ms": int((time.perf_counter() - t0) * 1000)}
