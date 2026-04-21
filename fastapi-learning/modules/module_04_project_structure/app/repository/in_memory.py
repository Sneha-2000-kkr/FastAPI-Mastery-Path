from itertools import count
from threading import Lock

from app.core.exceptions import InsufficientStock
from app.models.customer import Customer
from app.models.order import Order


class InMemoryCustomerRepo:
    def __init__(self) -> None:
        self._store: dict[int, Customer] = {}
        self._ids = count(1)
        self._lock = Lock()

    def get(self, customer_id: int) -> Customer | None:
        return self._store.get(customer_id)

    def add(self, *, email: str, name: str) -> Customer:
        with self._lock:
            cid = next(self._ids)
            c = Customer(id=cid, email=email, name=name)
            self._store[cid] = c
            return c

    def list(self) -> list[Customer]:
        return list(self._store.values())


class InMemoryOrderRepo:
    def __init__(self) -> None:
        self._store: dict[int, Order] = {}
        self._ids = count(1)
        self._lock = Lock()

    def add(self, order: Order) -> Order:
        with self._lock:
            order.id = next(self._ids)
            self._store[order.id] = order
            return order

    def get(self, order_id: int) -> Order | None:
        return self._store.get(order_id)

    def list_for_customer(self, customer_id: int) -> list[Order]:
        return [o for o in self._store.values() if o.customer_id == customer_id]


class InMemoryStockRepo:
    def __init__(self) -> None:
        self._stock: dict[str, int] = {"SKU-A": 100, "SKU-B": 25, "SKU-C": 5}
        self._price: dict[str, int] = {"SKU-A": 1500, "SKU-B": 4200, "SKU-C": 9999}
        self._lock = Lock()

    def get_price(self, sku: str) -> int:
        return self._price.get(sku, 0)

    def get_stock(self, sku: str) -> int:
        return self._stock.get(sku, 0)

    def decrement(self, sku: str, qty: int) -> None:
        with self._lock:
            current = self._stock.get(sku, 0)
            if current < qty:
                raise InsufficientStock(f"insufficient stock for {sku}")
            self._stock[sku] = current - qty
