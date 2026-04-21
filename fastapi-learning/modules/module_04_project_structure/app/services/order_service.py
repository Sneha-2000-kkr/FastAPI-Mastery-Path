from app.core.exceptions import CustomerNotFound
from app.models.order import Order, OrderItem
from app.repository.uow import UnitOfWork
from app.schemas.order import OrderItemIn


class OrderService:
    def __init__(self, uow_factory) -> None:
        self._uow_factory = uow_factory

    def place_order(self, *, customer_id: int, items: list[OrderItemIn]) -> Order:
        with self._uow_factory() as uow:
            customer = uow.customers.get(customer_id)
            if customer is None:
                raise CustomerNotFound(f"customer {customer_id} not found")

            order_items: list[OrderItem] = []
            for item in items:
                price = uow.stock.get_price(item.sku)
                uow.stock.decrement(item.sku, item.qty)  # raises InsufficientStock
                order_items.append(OrderItem(sku=item.sku, qty=item.qty, unit_price_cents=price))

            order = Order(id=0, customer_id=customer_id, items=order_items)
            saved = uow.orders.add(order)
            uow.commit()
            return saved

    def get(self, order_id: int) -> Order | None:
        with self._uow_factory() as uow:
            return uow.orders.get(order_id)
