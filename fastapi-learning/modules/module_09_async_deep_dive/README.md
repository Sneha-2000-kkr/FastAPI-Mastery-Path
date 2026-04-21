# Module 09 — Async Programming Deep Dive

How asyncio works, when to await, how `gather`/`TaskGroup` work, structured
concurrency, and offloading CPU-bound work.

Endpoints:
- `GET /fanout`        — calls 3 fake services concurrently with `asyncio.gather`
- `GET /fanout-tg`     — same with Python 3.11 `TaskGroup`
- `GET /timeout`       — demos `asyncio.timeout`
- `GET /cpu`           — offloads CPU work to a process pool
