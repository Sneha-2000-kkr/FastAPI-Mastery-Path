import logging

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.errors import register_exception_handlers
from app.core.middleware import (
    BodySizeLimitMiddleware,
    RequestIdMiddleware,
    TimingMiddleware,
)
from app.routes import demo


def create_app() -> FastAPI:
    logging.basicConfig(level=logging.INFO)
    s = get_settings()
    app = FastAPI(title=s.app_name, version=s.version)

    # Add OUTER first → INNER last; runtime order = top-to-bottom in code.
    app.add_middleware(BodySizeLimitMiddleware, max_bytes=s.max_body_bytes)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(RequestIdMiddleware)

    register_exception_handlers(app)
    app.include_router(demo.router)
    return app


app = create_app()
