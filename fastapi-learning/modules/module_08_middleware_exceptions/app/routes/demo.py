import asyncio
from typing import Any

from fastapi import APIRouter

from app.core.errors import NotFound

router = APIRouter(tags=["demo"])


@router.get("/ping")
async def ping() -> dict:
    return {"pong": True}


@router.get("/slow")
async def slow() -> dict:
    await asyncio.sleep(1.5)
    return {"slow": True}


@router.get("/boom")
async def boom():
    raise NotFound("nothing here")


@router.post("/echo")
async def echo(payload: dict[str, Any]) -> dict:
    return {"received": payload}
