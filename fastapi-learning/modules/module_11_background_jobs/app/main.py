import logging

from fastapi import FastAPI

from app.core.config import get_settings
from app.routes import jobs, notify


def create_app() -> FastAPI:
    logging.basicConfig(level=logging.INFO)
    s = get_settings()
    app = FastAPI(title=s.app_name, version=s.version)
    app.include_router(jobs.router)
    app.include_router(notify.router)
    return app


app = create_app()
