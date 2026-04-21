# Lesson 05 — PostgreSQL + Async SQLAlchemy 2.0

## 1. Concept Deep Dive

SQLAlchemy 2.0 has two sides:
- **Core** — SQL expression language, schema definitions.
- **ORM** — declarative `Mapped`/`mapped_column` classes built on Core.

The async stack:
- `create_async_engine(url)` returns an `AsyncEngine` — a pool of connections + a dialect.
- `async_sessionmaker(engine, expire_on_commit=False)` is a factory of `AsyncSession` instances.
- An `AsyncSession` wraps a connection and a transaction. **Always use one session per request** — created and closed in a `yield` dependency.

`expire_on_commit=False` is critical for FastAPI: after `commit()`, the default ORM behaviour expires every loaded attribute, which forces a refetch on the next access. Inside a route that reads attributes after commit (to serialize), that refetch happens *after* the session is closed → `MissingGreenlet` errors. Disable it.

### Identity map & flush
The session has an **identity map**: same primary key → same Python object within a session. `add()` stages an insert in the unit-of-work; `flush()` sends pending changes; `commit()` flushes + commits the transaction.

### Async vs sync
The async dialect uses `asyncpg`. Driver selection is via the URL prefix: `postgresql+asyncpg://...`. Don't mix `psycopg2` here.

## 2. Production Code Walkthrough

- `core/config.py` — reads `APP_DATABASE_URL`.
- `core/db.py` — engine, sessionmaker, lifespan-managed `dispose()`, `get_session` dependency.
- `models/item.py` — `Mapped[int]`, `mapped_column(...)`. Declarative base via `DeclarativeBase`.
- `repository/item_repository.py` — async repository. Uses `select(Item)` rather than legacy `Query`.
- `services/item_service.py` — same shape as module 01, swapped storage.
- `routes/items.py` — uses `AsyncSession` injected via the DB dep.

## 3. Why This Matters

Async DB access lets a single Uvicorn worker handle thousands of concurrent connections without blocking. The repository pattern means business logic doesn't change when storage does.

## 4. Common Mistakes

- **Sharing one engine across event loops.** Per-process is fine; per-worker for Gunicorn is correct.
- **Forgetting `expire_on_commit=False`.** See above.
- **Not closing the session.** Use a `yield` dep — the `finally` always runs.
- **Lazy loading with relationships in async.** SQLAlchemy will raise unless you eagerly load via `selectinload`/`joinedload`. There is no implicit IO in async ORM.
- **Running blocking SQL inside `async def`.** `session.execute(text(...))` IS async — but `engine.connect()` (sync) is not. Always use the async API.
- **Pool exhaustion**: default `pool_size=5`. In a 4-worker Uvicorn under load you have 20 connections — plan accordingly. Tune `pool_size` and `max_overflow`.

## 5. Senior-Level Insights

- **Use a single transaction per request.** `session.begin()` as a context manager wraps everything; on exception it rolls back automatically.
- **Migrations**: `Base.metadata.create_all` is for dev only. Use **Alembic** in any environment that has data you can't lose.
- **N+1**: load relationships with `selectinload`. Profile with `echo=True` and prefer SQL-level aggregates (`func.count`, window functions) over Python loops.
- **Prepared statements**: asyncpg caches them automatically; explicit naming helps when using PgBouncer in transaction-pooling mode (which can break prepared statements — set `prepared_statement_cache_size=0`).
- **Read replicas**: bind a separate engine + sessionmaker for read traffic; use FastAPI `Depends` to pick which one.

## 6. Hands-on Task

Add a unique constraint on `Item.name`. Catch `IntegrityError` in the service and raise a `ConflictError` translated to 409.

## 7. Mini Project

Add Alembic with one revision that creates `items`. Wire `alembic upgrade head` into the README run instructions and remove the `create_all` startup call.
