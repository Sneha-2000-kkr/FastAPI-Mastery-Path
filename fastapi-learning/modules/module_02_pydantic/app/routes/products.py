from fastapi import APIRouter, Body, Depends, status

from app.dependencies.common import get_product_service
from app.schemas.product import Product, ProductCreate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED,
             response_model_by_alias=True)
def create_product(payload: ProductCreate = Body(...),
                   service: ProductService = Depends(get_product_service)):
    return service.create(payload.model_dump(by_alias=False))


@router.get("", response_model=list[Product], response_model_by_alias=True)
def list_products(service: ProductService = Depends(get_product_service)):
    return service.list()
