import pytest


@pytest.mark.asyncio
async def test_create_then_get(client):
    r = await client.post("/items", json={"name": "book", "price_cents": 1500})
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["id"] == 1

    r = await client.get(f"/items/{item['id']}")
    assert r.status_code == 200
    assert r.json()["name"] == "book"


@pytest.mark.asyncio
async def test_get_missing_returns_404(client):
    r = await client.get("/items/999")
    assert r.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"name": "x"},
        {"name": "x", "price_cents": -1},
        {"name": "", "price_cents": 1},
    ],
)
async def test_validation_errors(client, payload):
    r = await client.post("/items", json=payload)
    assert r.status_code == 422
