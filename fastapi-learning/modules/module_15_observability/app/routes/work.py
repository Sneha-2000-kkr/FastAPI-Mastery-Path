import asyncio
import logging

from fastapi import APIRouter, Query

from app.core.metrics import metrics_response

router = APIRouter(tags=["observability"])
log = logging.getLogger(__name__)


@router.get("/work")
async def do_work(ms: int = Query(100, ge=0, le=5000)) -> dict:
    log.info("work.start", extra={"ctx_ms": ms})
    await asyncio.sleep(ms / 1000)
    log.info("work.done", extra={"ctx_ms": ms})
    return {"slept_ms": ms}


@router.get("/metrics", include_in_schema=False)
def metrics():
    return metrics_response()


@router.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
