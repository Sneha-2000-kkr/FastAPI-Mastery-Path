# Lesson 08 — Middleware & Exception Handling

## 1. Concept Deep Dive

### Middleware
Starlette middleware is built around the ASGI `(scope, receive, send)` triple. A `BaseHTTPMiddleware` simplifies it to a coroutine `dispatch(request, call_next)`. Middleware runs in **registration-reverse order**: the *last added* middleware is the **outermost** wrapper.

```
client → MW3 → MW2 → MW1 → router → handler
                 ↑
        (added first; innermost)
```

### Exception handling
FastAPI ships handlers for `HTTPException`, `RequestValidationError`, and a generic 500. Override them with `@app.exception_handler(ExcCls)`. **Don't** translate domain errors deep in the routes — register one handler per error class and let the system do the work.

Order of resolution:
1. Most specific exception class (subclass match).
2. Falls back to base `Exception` handler if any.
3. Else returns a generic 500.

### Body-size limit
There's no built-in limit. A 1 GB JSON POST will OOM your worker. Add a middleware that reads `Content-Length` and rejects early.

## 2. Production Code Walkthrough

- `core/middleware.py`:
  - `RequestIdMiddleware` — assigns or echoes `X-Request-ID`.
  - `TimingMiddleware` — adds `X-Process-Time-ms`.
  - `BodySizeLimitMiddleware` — rejects `> max_bytes` with 413.
- `core/errors.py` — `DomainError` hierarchy + `register_exception_handlers(app)` returning the **uniform error envelope** `{error: {code, message, details, request_id}}`.
- `routes/demo.py` — endpoints that exercise each path.
- `main.py` — installs middleware in the right order (outermost first in code = innermost at runtime; we add in reverse to read top-to-bottom).

## 3. Why This Matters

A predictable error contract is what lets a client team write a useful retry/UX. Logs without a request id are useless across services. Body limits are the cheapest DoS defense.

## 4. Common Mistakes

- **Catching exceptions in handlers and returning 200 with `{"error": ...}`.** Loses HTTP semantics. Use proper status codes.
- **Logging the request body in middleware.** Leaks PII / secrets. Log shape, not content.
- **Mutating `request.state` deep in business logic.** It's fine, but don't make it a hidden parameter — pass it explicitly.
- **Adding heavy work in middleware.** It runs on every request; profile carefully.
- **Forgetting to register exception handlers in tests** — test client uses the same app, but make sure `create_app()` is the single source of truth.

## 5. Senior-Level Insights

- For low-overhead per-request work, prefer **pure ASGI middleware** (a callable taking `(app)` and returning `(scope, receive, send)`) over `BaseHTTPMiddleware`. The latter spawns an extra task per request and breaks streaming.
- Use **structlog** (module 15) and bind `request_id` into the contextvar so every log line in the request gets it for free.
- For **GZip**, use Starlette's `GZipMiddleware` only when most responses compress well; small JSON gets larger.
- For **CORS**, prefer the strictest possible config; never use `*` with credentials (it's silently rejected by browsers).
- Define your **error envelope once** at the gateway level so every client sees the same shape regardless of which service responded.

## 6. Hands-on Task

Add a `RateLimitMiddleware` (token bucket per IP) that returns 429 with `Retry-After` when exceeded.

## 7. Mini Project

Add `ProblemDetails` (RFC 7807) format as an alternative error envelope, switchable via `Accept: application/problem+json`.
