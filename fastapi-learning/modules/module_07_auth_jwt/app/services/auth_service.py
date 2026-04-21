from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repository.user_repository import UserRepository


class InvalidCredentials(Exception):
    pass


class EmailAlreadyUsed(Exception):
    pass


class AuthService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def register(self, *, email: str, password: str, roles: list[str] | None = None) -> User:
        try:
            return self.repo.add(email=email, password_hash=hash_password(password), roles=roles)
        except ValueError:
            raise EmailAlreadyUsed(email)

    def authenticate(self, *, email: str, password: str) -> User:
        user = self.repo.get_by_email(email)
        # Always verify even if user is None (constant-time defense).
        valid = verify_password(password, user.password_hash if user else None)
        if not user or not valid or not user.is_active:
            raise InvalidCredentials()
        return user
