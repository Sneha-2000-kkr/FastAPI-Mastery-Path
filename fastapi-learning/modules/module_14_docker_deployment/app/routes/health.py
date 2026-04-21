from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/healthz")
def healthz() -> dict:
    s = get_settings()
    return {"status": "ok", "name": s.app_name, "version": s.version}


@router.get("/readyz")
def readyz() -> dict:
    # In a real app: check DB/Redis pings here and return non-200 if unhealthy.
    return {"ready": True}
