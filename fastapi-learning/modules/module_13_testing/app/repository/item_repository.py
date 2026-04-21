from itertools import count
from threading import Lock
from typing import Optional, Protocol

from app.models.item import Item


class ItemRepo(Protocol):
    def add(self, *, name: str, price_cents: int) -> Item: ...
    def get(self, item_id: int) -> Optional[Item]: ...
    def list(self) -> list[Item]: ...


class InMemoryItemRepo:
    def __init__(self) -> None:
        self._store: dict[int, Item] = {}
        self._ids = count(1)
        self._lock = Lock()

    def add(self, *, name: str, price_cents: int) -> Item:
        with self._lock:
            iid = next(self._ids)
            item = Item(id=iid, name=name, price_cents=price_cents)
            self._store[iid] = item
            return item

    def get(self, item_id: int) -> Optional[Item]:
        return self._store.get(item_id)

    def list(self) -> list[Item]:
        return list(self._store.values())


_repo = InMemoryItemRepo()


def get_item_repo() -> ItemRepo:
    return _repo
