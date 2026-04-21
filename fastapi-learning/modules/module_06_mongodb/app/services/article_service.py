from typing import Any

from app.repository.article_repository import ArticleRepository


class ArticleNotFound(Exception):
    pass


class ArticleService:
    def __init__(self, repo: ArticleRepository) -> None:
        self.repo = repo

    async def list(self, *, limit: int, skip: int) -> list[dict[str, Any]]:
        return await self.repo.list(limit=limit, skip=skip)

    async def get(self, article_id: str) -> dict[str, Any]:
        doc = await self.repo.get(article_id)
        if doc is None:
            raise ArticleNotFound(article_id)
        return doc

    async def create(self, **kwargs) -> dict[str, Any]:
        return await self.repo.create(**kwargs)

    async def update(self, article_id: str, patch: dict[str, Any]) -> dict[str, Any]:
        doc = await self.repo.update(article_id, patch)
        if doc is None:
            raise ArticleNotFound(article_id)
        return doc

    async def delete(self, article_id: str) -> None:
        if not await self.repo.delete(article_id):
            raise ArticleNotFound(article_id)
