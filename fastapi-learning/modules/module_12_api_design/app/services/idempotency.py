import hashlib
import time
from threading import Lock
from typing import Any

from app.core.config import get_settings


def hash_body(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


class IdempotencyStore:
    def __init__(self) -> None:
        # key -> (body_hash, response, expires_at)
        self._store: dict[str, tuple[str, Any, float]] = {}
        self._lock = Lock()

    def get(self, key: str) -> tuple[str, Any] | None:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            body_hash, resp, exp = entry
            if exp < time.time():
                self._store.pop(key, None)
                return None
            return body_hash, resp

    def put(self, key: str, body_hash: str, response: Any) -> None:
        ttl = get_settings().idempotency_ttl_seconds
        with self._lock:
            self._store[key] = (body_hash, response, time.time() + ttl)


_store = IdempotencyStore()


def get_idempotency_store() -> IdempotencyStore:
    return _store
