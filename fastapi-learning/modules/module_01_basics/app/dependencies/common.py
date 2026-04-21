from __future__ import annotations

from dataclasses import dataclass

from fastapi import Query

from app.repository.item_repository import ItemRepository, get_item_repository
from app.services.item_service import ItemService


@dataclass
class Pagination:
    limit: int
    offset: int


def pagination_params(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> Pagination:
    return Pagination(limit=limit, offset=offset)


def get_item_service() -> ItemService:
    return ItemService(get_item_repository())
