from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.db import Base, engine
from app.routes import items


@asynccontextmanager
async def lifespan(app: FastAPI):
    # DEV ONLY — use Alembic in any environment with data you can't lose
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    s = get_settings()
    app = FastAPI(title=s.app_name, version=s.version, lifespan=lifespan)
    app.include_router(items.router)
    return app


app = create_app()
