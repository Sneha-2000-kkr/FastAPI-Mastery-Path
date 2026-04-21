"""Yield-based dependency demo using a fake 'connection'."""
from typing import Iterator
import logging

log = logging.getLogger("db_demo")


class FakeConn:
    def __init__(self, name: str) -> None:
        self.name = name
        self.closed = False

    def query(self, sql: str) -> str:
        if self.closed:
            raise RuntimeError("connection closed")
        return f"[{self.name}] -> {sql}"


def get_conn() -> Iterator[FakeConn]:
    conn = FakeConn(name="conn-1")
    log.info("opening %s", conn.name)
    try:
        yield conn
    finally:
        conn.closed = True
        log.info("closing %s", conn.name)
