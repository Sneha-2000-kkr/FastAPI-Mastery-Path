from fastapi import APIRouter, Depends, HTTPException, status

from app.core.exceptions import DomainError
from app.dependencies.common import get_order_service
from app.schemas.order import OrderCreate, OrderItemOut, OrderRead
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


def _to_read(order) -> OrderRead:
    return OrderRead(
        id=order.id,
        customer_id=order.customer_id,
        status=order.status,
        items=[
            OrderItemOut(
                sku=i.sku, qty=i.qty,
                unit_price_cents=i.unit_price_cents,
                total_cents=i.total_cents,
            )
            for i in order.items
        ],
        total_cents=order.total_cents,
    )


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def place(payload: OrderCreate, svc: OrderService = Depends(get_order_service)):
    try:
        order = svc.place_order(customer_id=payload.customer_id, items=payload.items)
    except DomainError as e:
        raise HTTPException(status_code=e.http_status, detail={"code": e.code, "message": str(e)})
    return _to_read(order)


@router.get("/{order_id}", response_model=OrderRead)
def get(order_id: int, svc: OrderService = Depends(get_order_service)):
    order = svc.get(order_id)
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="order not found")
    return _to_read(order)
