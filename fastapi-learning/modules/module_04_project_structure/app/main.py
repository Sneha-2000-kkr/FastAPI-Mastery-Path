from fastapi import FastAPI

from app.core.config import get_settings
from app.routes import customers, orders


def create_app() -> FastAPI:
    s = get_settings()
    app = FastAPI(title=s.app_name, version=s.version)
    app.include_router(customers.router)
    app.include_router(orders.router)
    return app


app = create_app()
