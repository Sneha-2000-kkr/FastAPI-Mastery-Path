from fastapi import FastAPI

from app.core.config import get_settings
from app.routes import posts_v1


def create_app() -> FastAPI:
    s = get_settings()
    app = FastAPI(title=s.app_name, version=s.version)
    app.include_router(posts_v1.router)
    return app


app = create_app()
