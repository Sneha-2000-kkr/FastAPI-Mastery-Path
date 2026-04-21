from fastapi import Depends

from app.repository.item_repository import ItemRepo, get_item_repo
from app.services.item_service import ItemService


def get_item_service(repo: ItemRepo = Depends(get_item_repo)) -> ItemService:
    return ItemService(repo)
