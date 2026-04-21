import hashlib

from app.models.user import User
from app.repository.user_repository import UserRepository


def _hash(pw: str) -> str:
    # placeholder — real hashing happens in module 07
    return hashlib.sha256(pw.encode()).hexdigest()


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def create(self, *, email: str, password: str, first_name: str, last_name: str) -> User:
        return self.repo.add(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=_hash(password),
        )
