# Lesson 01 — FastAPI Basics & The Request Lifecycle

## 1. Concept Deep Dive

FastAPI is a thin layer on top of **Starlette** (ASGI framework) and **Pydantic** (data validation). When you write:

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int): ...
```

a number of things happen at **import time** and at **request time**.

### Import time
1. `FastAPI()` creates an ASGI app — really a Starlette `Router` plus an OpenAPI generator.
2. The decorator inspects your handler with `inspect.signature(...)`. For each parameter it builds a **Dependant** tree describing where the value comes from: path param, query param, header, body, or `Depends(...)`.
3. Type hints are converted to Pydantic field types and cached. The OpenAPI schema is built lazily on first access to `/openapi.json`.

### Request time (per request)
1. Uvicorn receives bytes, parses the HTTP frame, and invokes the ASGI callable with `scope`, `receive`, `send`.
2. Starlette's middleware stack runs (outer → inner). Each middleware can short-circuit or pass through.
3. The router matches the path → finds the handler → resolves the **Dependant** tree:
   - path/query/header values are coerced and validated by Pydantic
   - body is read from `receive()` (one or more chunks), parsed (json/form/multipart), then validated
   - `Depends(...)` callables are invoked in topological order; results are cached **per-request** by `(callable, scope)`
4. Your handler runs (sync handlers go to a thread pool; async handlers run on the event loop).
5. The return value is serialized via `jsonable_encoder` and wrapped into a `JSONResponse` (unless you return a `Response` directly).
6. Response middlewares run (inner → outer), headers are written, body chunks are sent.

> **Mental model**: FastAPI = Starlette router + Pydantic-driven introspection + auto-generated OpenAPI. Every "magic" feature is just signature inspection plus generated validators.

## 2. Production Code Walkthrough

- `app/core/config.py` — single `Settings` object loaded from env vars via `pydantic-settings`. **Never** read `os.environ` scattered through your code.
- `app/main.py` — application factory `create_app()` so tests can build an isolated app instance.
- `app/routes/items.py` — `APIRouter` mounted under `/items`. Handlers stay thin: parse → call service → return.
- `app/services/item_service.py` — business logic. The handler does not know how items are stored.
- `app/repository/item_repository.py` — storage. Today it's an in-memory dict; module 05 swaps it for Postgres without touching routes.
- `app/schemas/item.py` — request/response models. **Schemas are not the same as DB models.**
- `app/dependencies/common.py` — pagination dependency.

## 3. Why This Matters

In a real backend:
- The HTTP layer is the *thinnest* part of your code. It exists only to translate HTTP ⇄ domain calls.
- Business logic lives in services so it can be reused by HTTP, CLI, and background workers.
- Storage hides behind a repository so you can swap Postgres ↔ Mongo ↔ in-memory without touching the rest of the system.

This separation is overkill for a 1-file demo and exactly right for anything that ships.

## 4. Common Mistakes

- **Putting DB calls in the handler.** Hard to test, impossible to reuse from a worker.
- **Returning ORM objects directly.** Leaks columns you didn't mean to expose (e.g. `password_hash`). Always project to a response schema.
- **Using sync `def` handlers that call blocking I/O.** Sync handlers execute in a thread pool of size 40 by default — under load you exhaust the pool and the event loop stalls.
- **Catching `Exception` in handlers.** Hides bugs. Let exception handlers (module 08) shape the response.
- **Hard-coding config.** Use `Settings`. Module 04 expands on this.

## 5. Senior-Level Insights

- **Sync vs async handlers**: prefer `async def`. Use `def` only when the work is purely CPU-bound and short, or when you must call a blocking C-extension and there is no async alternative. Mixing the two is fine; FastAPI handles it.
- **Path operation order matters**: more specific routes must be declared **before** more general ones (`/items/me` before `/items/{id}`).
- **`response_model` does double duty**: it validates the response *and* trims unknown fields. This is a security boundary, not a convenience.
- **Avoid `from app import *`** — it breaks the import-time signature inspection because of forward references.
- **`response_model_exclude_none=True`** is a footgun: clients then can't distinguish "absent" from "null" — important in PATCH semantics.

## 6. Hands-on Task

Add a `PATCH /items/{item_id}` endpoint that accepts a partial `ItemUpdate` schema (all fields optional) and updates only the provided keys. The handler must remain a thin wrapper that delegates to a new `update_item` service method.

## 7. Mini Project

Extend the in-memory repository with a `search(q: str)` method and expose `GET /items/search?q=...`. Returns items whose `name` contains the query (case-insensitive). Add a `total` field in the response using the shared `Page` model from `shared/pagination.py`.
