from itertools import count
from threading import Lock
from typing import Optional

from app.models.user import User


class UserRepository:
    def __init__(self) -> None:
        self._store: dict[int, User] = {}
        self._by_email: dict[str, int] = {}
        self._ids = count(1)
        self._lock = Lock()

    def add(self, *, email: str, first_name: str, last_name: str, password_hash: str) -> User:
        with self._lock:
            if email in self._by_email:
                raise ValueError("email already used")
            uid = next(self._ids)
            user = User(id=uid, email=email, first_name=first_name,
                        last_name=last_name, password_hash=password_hash)
            self._store[uid] = user
            self._by_email[email] = uid
            return user

    def get(self, uid: int) -> Optional[User]:
        return self._store.get(uid)


_repo = UserRepository()


def get_user_repository() -> UserRepository:
    return _repo
