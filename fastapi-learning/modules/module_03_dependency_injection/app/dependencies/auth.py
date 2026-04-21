from dataclasses import dataclass
from fastapi import Header, HTTPException, status, Depends


@dataclass
class CurrentUser:
    id: int
    email: str
    is_active: bool


def get_current_user(x_user: str | None = Header(default=None)) -> CurrentUser:
    """Toy auth: header `X-User: 1:alice@example.com:1`."""
    if not x_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "missing X-User header")
    try:
        uid, email, active = x_user.split(":")
        return CurrentUser(id=int(uid), email=email, is_active=bool(int(active)))
    except (ValueError, TypeError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "malformed X-User header")


def get_active_user(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "user is inactive")
    return user
