from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.repository.item_repository import ItemRepository
from app.services.item_service import ItemService


def get_item_service(session: AsyncSession = Depends(get_session)) -> ItemService:
    return ItemService(ItemRepository(session))


def pagination(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> tuple[int, int]:
    return limit, offset
