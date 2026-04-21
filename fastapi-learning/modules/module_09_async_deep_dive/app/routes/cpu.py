import asyncio

from fastapi import APIRouter, Request

from app.services.cpu import count_primes

router = APIRouter(tags=["async"])


@router.get("/cpu")
async def cpu(upto: int, request: Request) -> dict:
    pool = request.app.state.cpu_pool
    loop = asyncio.get_running_loop()
    primes = await loop.run_in_executor(pool, count_primes, upto)
    return {"upto": upto, "primes": primes}
