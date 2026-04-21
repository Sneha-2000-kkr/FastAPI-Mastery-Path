import logging

from fastapi import FastAPI

from app.core.config import get_settings
from app.routes import db_demo, me, reports


def create_app() -> FastAPI:
    logging.basicConfig(level=logging.INFO)
    s = get_settings()
    app = FastAPI(title=s.app_name, version=s.version)
    app.include_router(me.router)
    app.include_router(reports.router)
    app.include_router(db_demo.router)
    return app


app = create_app()
