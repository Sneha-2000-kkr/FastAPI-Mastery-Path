from app.models.customer import Customer
from app.repository.protocols import CustomerRepo


class CustomerService:
    def __init__(self, repo: CustomerRepo) -> None:
        self.repo = repo

    def create(self, *, email: str, name: str) -> Customer:
        return self.repo.add(email=email, name=name)

    def list(self) -> list[Customer]:
        return self.repo.list()
