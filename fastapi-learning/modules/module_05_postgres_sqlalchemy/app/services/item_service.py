from typing import Optional

from app.models.item import Item
from app.repository.item_repository import ItemRepository


class ItemNotFound(Exception):
    pass


class ItemService:
    def __init__(self, repo: ItemRepository) -> None:
        self.repo = repo

    async def list(self, *, limit: int, offset: int) -> tuple[list[Item], int]:
        return await self.repo.list(limit=limit, offset=offset)

    async def get(self, item_id: int) -> Item:
        item = await self.repo.get(item_id)
        if item is None:
            raise ItemNotFound(f"item {item_id}")
        return item

    async def create(self, *, name: str, description: Optional[str], price_cents: int) -> Item:
        return await self.repo.add(name=name, description=description, price_cents=price_cents)

    async def delete(self, item_id: int) -> None:
        if not await self.repo.delete(item_id):
            raise ItemNotFound(f"item {item_id}")
