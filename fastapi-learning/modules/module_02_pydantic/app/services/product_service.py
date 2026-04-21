from typing import Any

from app.repository.product_repository import ProductRepository


class ProductService:
    def __init__(self, repo: ProductRepository) -> None:
        self.repo = repo

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.repo.add(payload)

    def list(self) -> list[dict[str, Any]]:
        return self.repo.list()
