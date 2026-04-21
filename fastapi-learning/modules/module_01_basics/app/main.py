from __future__ import annotations

from fastapi import FastAPI

from app.core.config import get_settings
from app.routes import health, items


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.version, debug=settings.debug)
    app.include_router(health.router)
    app.include_router(items.router)
    return app


app = create_app()
