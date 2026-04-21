import pytest

from app.repository.item_repository import InMemoryItemRepo
from app.services.item_service import ItemNotFound, ItemService


def test_create_and_get():
    svc = ItemService(InMemoryItemRepo())
    item = svc.create(name="laptop", price_cents=199900)
    assert item.id == 1
    assert svc.get(item.id).name == "laptop"


def test_get_missing_raises():
    svc = ItemService(InMemoryItemRepo())
    with pytest.raises(ItemNotFound):
        svc.get(999)


def test_negative_price_rejected():
    svc = ItemService(InMemoryItemRepo())
    with pytest.raises(ValueError):
        svc.create(name="x", price_cents=-1)
