from fastapi import FastAPI

from app.core.config import get_settings
from app.routes import products, users


def create_app() -> FastAPI:
    s = get_settings()
    app = FastAPI(title=s.app_name, version=s.version)
    app.include_router(users.router)
    app.include_router(products.router)
    return app


app = create_app()
