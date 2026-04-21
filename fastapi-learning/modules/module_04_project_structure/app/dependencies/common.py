from app.repository.in_memory import (
    InMemoryCustomerRepo,
    InMemoryOrderRepo,
    InMemoryStockRepo,
)
from app.repository.uow import UnitOfWork
from app.services.customer_service import CustomerService
from app.services.order_service import OrderService

_customers = InMemoryCustomerRepo()
_orders = InMemoryOrderRepo()
_stock = InMemoryStockRepo()


def _uow_factory() -> UnitOfWork:
    return UnitOfWork(_customers, _orders, _stock)


def get_customer_service() -> CustomerService:
    return CustomerService(_customers)


def get_order_service() -> OrderService:
    return OrderService(_uow_factory)
