from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.dependencies.common import get_item_service, pagination
from app.schemas.item import ItemCreate, ItemRead
from app.services.item_service import ItemNotFound, ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemRead])
async def list_items(page=Depends(pagination), svc: ItemService = Depends(get_item_service)):
    limit, offset = page
    items, _ = await svc.list(limit=limit, offset=offset)
    return items


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(item_id: int, svc: ItemService = Depends(get_item_service)):
    try:
        return await svc.get(item_id)
    except ItemNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    payload: ItemCreate,
    svc: ItemService = Depends(get_item_service),
    session: AsyncSession = Depends(get_session),
):
    item = await svc.create(**payload.model_dump())
    await session.commit()
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    svc: ItemService = Depends(get_item_service),
    session: AsyncSession = Depends(get_session),
):
    try:
        await svc.delete(item_id)
        await session.commit()
    except ItemNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
