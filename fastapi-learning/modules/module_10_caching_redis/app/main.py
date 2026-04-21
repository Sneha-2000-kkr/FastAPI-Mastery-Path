from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.redis_client import close, init
from app.routes import quotes


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()
    yield
    await close()


def create_app() -> FastAPI:
    s = get_settings()
    app = FastAPI(title=s.app_name, version=s.version, lifespan=lifespan)
    app.include_router(quotes.router)
    return app


app = create_app()
