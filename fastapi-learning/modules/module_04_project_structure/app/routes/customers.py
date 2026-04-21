from fastapi import APIRouter, Depends, status

from app.dependencies.common import get_customer_service
from app.schemas.customer import CustomerCreate, CustomerRead
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create(payload: CustomerCreate, svc: CustomerService = Depends(get_customer_service)):
    return svc.create(email=payload.email, name=payload.name)


@router.get("", response_model=list[CustomerRead])
def list_(svc: CustomerService = Depends(get_customer_service)):
    return svc.list()
