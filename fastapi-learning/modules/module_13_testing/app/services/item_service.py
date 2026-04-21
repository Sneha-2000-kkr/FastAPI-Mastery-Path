from app.models.item import Item
from app.repository.item_repository import ItemRepo


class ItemNotFound(Exception):
    pass


class ItemService:
    def __init__(self, repo: ItemRepo) -> None:
        self.repo = repo

    def create(self, *, name: str, price_cents: int) -> Item:
        if price_cents < 0:
            raise ValueError("price must be non-negative")
        return self.repo.add(name=name, price_cents=price_cents)

    def get(self, item_id: int) -> Item:
        item = self.repo.get(item_id)
        if item is None:
            raise ItemNotFound(item_id)
        return item

    def list(self) -> list[Item]:
        return self.repo.list()
