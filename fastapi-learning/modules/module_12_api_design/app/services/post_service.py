from dataclasses import dataclass, field
from datetime import datetime, timezone
from itertools import count
from threading import Lock
from typing import Optional

from app.core.etag import strong_etag


@dataclass
class Post:
    id: int
    title: str
    body: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def etag(self) -> str:
        return strong_etag({"id": self.id, "title": self.title, "body": self.body,
                            "updated_at": self.updated_at.isoformat()})


class PostService:
    def __init__(self) -> None:
        self._store: dict[int, Post] = {}
        self._ids = count(1)
        self._lock = Lock()

    def list_cursor(self, *, after_id: Optional[int], limit: int) -> tuple[list[Post], Optional[int]]:
        items = sorted(self._store.values(), key=lambda p: p.id)
        if after_id is not None:
            items = [p for p in items if p.id > after_id]
        page = items[:limit]
        next_cursor = page[-1].id if len(page) == limit and len(items) > limit else None
        return page, next_cursor

    def get(self, post_id: int) -> Optional[Post]:
        return self._store.get(post_id)

    def create(self, *, title: str, body: str) -> Post:
        with self._lock:
            pid = next(self._ids)
            post = Post(id=pid, title=title, body=body)
            self._store[pid] = post
            return post

    def update(self, post_id: int, *, title: Optional[str], body: Optional[str]) -> Optional[Post]:
        with self._lock:
            post = self._store.get(post_id)
            if post is None:
                return None
            if title is not None:
                post.title = title
            if body is not None:
                post.body = body
            post.updated_at = datetime.now(timezone.utc)
            return post


_svc = PostService()


def get_post_service() -> PostService:
    return _svc
