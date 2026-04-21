from pydantic import BaseModel, Field

from app.models.order import OrderStatus


class OrderItemIn(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    qty: int = Field(gt=0, le=1000)


class OrderItemOut(BaseModel):
    sku: str
    qty: int
    unit_price_cents: int
    total_cents: int


class OrderCreate(BaseModel):
    customer_id: int
    items: list[OrderItemIn] = Field(min_length=1, max_length=100)


class OrderRead(BaseModel):
    id: int
    customer_id: int
    status: OrderStatus
    items: list[OrderItemOut]
    total_cents: int
