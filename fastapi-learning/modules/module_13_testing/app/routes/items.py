from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.common import get_item_service
from app.schemas.item import ItemCreate, ItemRead
from app.services.item_service import ItemNotFound, ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemRead])
def list_items(svc: ItemService = Depends(get_item_service)):
    return svc.list()


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, svc: ItemService = Depends(get_item_service)):
    try:
        return svc.get(item_id)
    except ItemNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "item not found")


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, svc: ItemService = Depends(get_item_service)):
    return svc.create(**payload.model_dump())
