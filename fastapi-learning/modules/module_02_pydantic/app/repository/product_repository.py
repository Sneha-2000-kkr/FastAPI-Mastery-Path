from itertools import count
from threading import Lock
from typing import Any


class ProductRepository:
    """Stores raw discriminated dicts; service is responsible for validating."""

    def __init__(self) -> None:
        self._store: dict[int, dict[str, Any]] = {}
        self._ids = count(1)
        self._lock = Lock()

    def add(self, payload: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            pid = next(self._ids)
            payload = {**payload, "id": pid}
            self._store[pid] = payload
            return payload

    def list(self) -> list[dict[str, Any]]:
        return list(self._store.values())


_repo = ProductRepository()


def get_product_repository() -> ProductRepository:
    return _repo
