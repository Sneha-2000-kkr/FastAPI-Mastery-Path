# Lesson 03 — Dependency Injection (Internals)

## 1. Concept Deep Dive

`Depends(callable)` is a marker. At route-registration time, FastAPI inspects every parameter; any parameter whose default is a `Depends(...)` is added to a **Dependant** node. Each callable's signature is itself inspected, recursively, building a DAG of dependencies.

At request time:
1. FastAPI walks the DAG depth-first.
2. For each callable, it builds the kwargs (path/query/header/body or recursive deps), invokes it, and stores the result in a per-request **dependency cache** keyed by `(callable, security_scopes)`. The cache means the same dependency is computed **once per request** by default; pass `Depends(fn, use_cache=False)` to opt out.
3. Callables defined as `def` run in a thread pool; `async def` run on the loop. `yield` callables are treated as context managers — the code before `yield` runs on entry, the code after `yield` runs on exit (success or failure), allowing finally-style cleanup. Multiple `yield` deps form a stack popped in reverse order.

### Scopes
Out of the box there is **only request scope**. There is no built-in singleton scope — the conventional pattern is:
- module-level singletons (clients, settings) created at import or in a lifespan
- a thin `get_x()` provider that returns the singleton; `Depends(get_x)` wires it in

### Class-based deps
`Depends(MyClass)` calls `MyClass(...)` per request, with `__init__` parameters resolved like any other dependency. Useful when several endpoints share a tuple of inputs (e.g. `DateRange`).

### Overrides
`app.dependency_overrides[real] = fake` swaps any callable in the DAG. This is the canonical way to inject test doubles — module 13 uses it.

## 2. Production Code Walkthrough

- `dependencies/auth.py` — `get_current_user` parses a fake header, `get_active_user` further checks `is_active`. Composition is just `Depends(get_current_user)`.
- `dependencies/range.py` — `DateRange` class with validators in `__init__`.
- `dependencies/db.py` — a `yield` dependency that opens and closes a fake DB connection. Demonstrates the try/yield/finally idiom.
- `routes/me.py`, `routes/reports.py`, `routes/db_demo.py` — pure consumers.

## 3. Why This Matters

DI is what keeps a FastAPI app **testable, layered, and async-safe**. Without it you end up importing repositories at module top, making mocking impossible and forcing global state.

## 4. Common Mistakes

- **Using globals for the DB session.** Each request needs its own session; `yield` deps make this trivial.
- **Holding state in module-level singletons that aren't thread-safe.** A Redis client is OK; a Postgres `Session` is not.
- **`Depends(MyClass())` instead of `Depends(MyClass)`.** The first creates one instance forever — almost always a bug.
- **Side effects in deps.** Logging is fine; DB writes are not.
- **Forgetting `use_cache=False`** when the dep should re-run (e.g. a fresh idempotency key).

## 5. Senior-Level Insights

- For app-wide resources (HTTP client, DB engine, Redis), prefer the FastAPI **lifespan** context (`@asynccontextmanager`) over import-time creation. Lifespan ties the resource to the app's lifecycle and lets it depend on settings.
- `Depends` resolves async deps on the loop — don't `asyncio.run(...)` inside a sync dep.
- For background tasks created via `BackgroundTasks`, the request-scoped DB session is **already closed** when they run. Inject a fresh session inside the task instead.
- Use sub-dependencies to enforce **policy at the edges**: `require_role("admin")` returning a callable lets you write `Depends(require_role("admin"))` per route.

## 6. Hands-on Task

Add a `RateLimit` class-based dependency that takes `max_per_minute: int` from a query string and stores hits per-IP in a `dict[str, list[float]]`. Reject with 429 when exceeded.

## 7. Mini Project

Build a `Depends`-driven feature flag system: `Depends(require_feature("beta_reports"))` returns the flag value or raises 404 if disabled. Flags are loaded from `Settings`.
