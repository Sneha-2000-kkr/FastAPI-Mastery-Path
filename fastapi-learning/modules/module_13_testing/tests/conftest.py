import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import create_app
from app.repository.item_repository import InMemoryItemRepo, get_item_repo


@pytest.fixture
def app():
    app = create_app()
    fake = InMemoryItemRepo()
    app.dependency_overrides[get_item_repo] = lambda: fake
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
