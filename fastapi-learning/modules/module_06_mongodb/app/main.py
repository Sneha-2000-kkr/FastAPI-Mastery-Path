from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.mongo import close_client, get_db, init_client
from app.repository.article_repository import ArticleRepository
from app.routes import articles


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_client()
    await ArticleRepository(get_db()).ensure_indexes()
    yield
    close_client()


def create_app() -> FastAPI:
    s = get_settings()
    app = FastAPI(title=s.app_name, version=s.version, lifespan=lifespan)
    app.include_router(articles.router)
    return app


app = create_app()
