import asyncio

from fastapi import APIRouter, HTTPException, status

router = APIRouter(tags=["async"])


@router.get("/timeout")
async def with_timeout(seconds: float = 0.5) -> dict:
    try:
        async with asyncio.timeout(seconds):
            await asyncio.sleep(1.0)
    except TimeoutError:
        raise HTTPException(status.HTTP_504_GATEWAY_TIMEOUT, "downstream timed out")
    return {"finished": True}
