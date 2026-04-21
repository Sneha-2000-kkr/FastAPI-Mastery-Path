from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.common import Pagination, get_item_service, pagination_params
from app.schemas.item import ItemCreate, ItemRead
from app.services.item_service import ItemNotFound, ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemRead])
def list_items(
    page: Pagination = Depends(pagination_params),
    service: ItemService = Depends(get_item_service),
) -> list:
    items, _total = service.list_items(limit=page.limit, offset=page.offset)
    return items


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, service: ItemService = Depends(get_item_service)):
    try:
        return service.get_item(item_id)
    except ItemNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, service: ItemService = Depends(get_item_service)):
    return service.create_item(**payload.model_dump())


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, service: ItemService = Depends(get_item_service)):
    try:
        service.delete_item(item_id)
    except ItemNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
