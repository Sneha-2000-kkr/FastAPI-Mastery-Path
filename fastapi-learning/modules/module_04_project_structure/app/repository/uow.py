"""Unit-of-work that snapshots/restores the in-memory stores. In modules
05/07 it becomes a real DB transaction."""
from contextlib import AbstractContextManager
import copy

from app.repository.in_memory import (
    InMemoryCustomerRepo,
    InMemoryOrderRepo,
    InMemoryStockRepo,
)


class UnitOfWork(AbstractContextManager):
    def __init__(
        self,
        customers: InMemoryCustomerRepo,
        orders: InMemoryOrderRepo,
        stock: InMemoryStockRepo,
    ) -> None:
        self.customers = customers
        self.orders = orders
        self.stock = stock
        self._snapshot: dict | None = None
        self._committed = False

    def __enter__(self) -> "UnitOfWork":
        # snapshot mutable state of every repo we manage
        self._snapshot = {
            "customers": copy.deepcopy(self.customers._store),
            "orders": copy.deepcopy(self.orders._store),
            "stock": copy.deepcopy(self.stock._stock),
        }
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc_type is not None or not self._committed:
            assert self._snapshot is not None
            self.customers._store = self._snapshot["customers"]
            self.orders._store = self._snapshot["orders"]
            self.stock._stock = self._snapshot["stock"]

    def commit(self) -> None:
        self._committed = True
