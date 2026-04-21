from __future__ import annotations

from typing import Optional

from app.models.item import Item
from app.repository.item_repository import ItemRepository


class ItemNotFound(Exception):
    def __init__(self, item_id: int) -> None:
        super().__init__(f"item {item_id} not found")
        self.item_id = item_id


class ItemService:
    def __init__(self, repo: ItemRepository) -> None:
        self.repo = repo

    def list_items(self, limit: int, offset: int) -> tuple[list[Item], int]:
        return self.repo.list(limit, offset)

    def get_item(self, item_id: int) -> Item:
        item = self.repo.get(item_id)
        if item is None:
            raise ItemNotFound(item_id)
        return item

    def create_item(self, *, name: str, description: Optional[str], price_cents: int) -> Item:
        return self.repo.add(name=name, description=description, price_cents=price_cents)

    def delete_item(self, item_id: int) -> None:
        if not self.repo.delete(item_id):
            raise ItemNotFound(item_id)
