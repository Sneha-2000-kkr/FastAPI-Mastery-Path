from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


@dataclass
class OrderItem:
    sku: str
    qty: int
    unit_price_cents: int

    @property
    def total_cents(self) -> int:
        return self.qty * self.unit_price_cents


@dataclass
class Order:
    id: int
    customer_id: int
    items: list[OrderItem]
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def total_cents(self) -> int:
        return sum(i.total_cents for i in self.items)
