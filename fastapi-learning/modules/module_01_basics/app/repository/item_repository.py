from __future__ import annotations

from itertools import count
from threading import Lock
from typing import Optional

from app.models.item import Item


class ItemRepository:
    """In-memory repository. Thread-safe enough for a single-process dev server."""

    def __init__(self) -> None:
        self._store: dict[int, Item] = {}
        self._ids = count(1)
        self._lock = Lock()

    def list(self, limit: int, offset: int) -> tuple[list[Item], int]:
        with self._lock:
            items = list(self._store.values())
            total = len(items)
        return items[offset : offset + limit], total

    def get(self, item_id: int) -> Optional[Item]:
        return self._store.get(item_id)

    def add(self, *, name: str, description: Optional[str], price_cents: int) -> Item:
        with self._lock:
            item_id = next(self._ids)
            item = Item(id=item_id, name=name, description=description, price_cents=price_cents)
            self._store[item_id] = item
            return item

    def update(self, item_id: int, **patch) -> Optional[Item]:
        with self._lock:
            item = self._store.get(item_id)
            if item is None:
                return None
            for k, v in patch.items():
                if v is not None:
                    setattr(item, k, v)
            return item

    def delete(self, item_id: int) -> bool:
        with self._lock:
            return self._store.pop(item_id, None) is not None


_repo = ItemRepository()


def get_item_repository() -> ItemRepository:
    """Singleton accessor — wired through Depends() in module 03."""
    return _repo
