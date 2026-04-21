from itertools import count
from threading import Lock

from app.models.user import User


class UserRepository:
    def __init__(self) -> None:
        self._by_id: dict[int, User] = {}
        self._by_email: dict[str, int] = {}
        self._ids = count(1)
        self._lock = Lock()

    def get_by_email(self, email: str) -> User | None:
        uid = self._by_email.get(email)
        return self._by_id.get(uid) if uid else None

    def get(self, uid: int) -> User | None:
        return self._by_id.get(uid)

    def add(self, *, email: str, password_hash: str, roles: list[str] | None = None) -> User:
        with self._lock:
            if email in self._by_email:
                raise ValueError("email already used")
            uid = next(self._ids)
            user = User(id=uid, email=email, password_hash=password_hash,
                        roles=roles or ["user"])
            self._by_id[uid] = user
            self._by_email[email] = uid
            return user

    def list(self) -> list[User]:
        return list(self._by_id.values())


_repo = UserRepository()


def get_user_repository() -> UserRepository:
    return _repo
