from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
_DUMMY_HASH = _pwd.hash("not-a-real-password-and-it-doesnt-matter")


def hash_password(plain: str) -> str:
    return _pwd.hash(plain)


def verify_password(plain: str, hashed: str | None) -> bool:
    # Always run a hash to keep timing constant — defeats user enumeration via timing.
    return _pwd.verify(plain, hashed or _DUMMY_HASH) if hashed else (
        _pwd.verify(plain, _DUMMY_HASH) and False
    )


def create_access_token(*, sub: str, roles: list[str]) -> tuple[str, int]:
    s = get_settings()
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=s.jwt_expires_min)
    payload: dict[str, Any] = {
        "sub": sub,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "iss": s.jwt_issuer,
        "aud": s.jwt_audience,
        "jti": uuid4().hex,
        "roles": roles,
    }
    token = jwt.encode(payload, s.jwt_secret, algorithm=s.jwt_alg)
    return token, s.jwt_expires_min * 60


def decode_token(token: str) -> dict[str, Any]:
    s = get_settings()
    return jwt.decode(
        token,
        s.jwt_secret,
        algorithms=[s.jwt_alg],
        audience=s.jwt_audience,
        issuer=s.jwt_issuer,
    )
