from app.core.mongo import get_db
from app.repository.article_repository import ArticleRepository
from app.services.article_service import ArticleService


def get_article_service() -> ArticleService:
    return ArticleService(ArticleRepository(get_db()))
