# Module 03 — Dependency Injection

How FastAPI's `Depends` actually works, scopes, sub-dependencies, `yield`-based
resource management, class-based dependencies, and `app.dependency_overrides`
for testing.

Endpoints:
- `GET /reports?from=...&to=...` — uses a class-based `DateRange` dependency
- `GET /me` — composes `get_current_user → get_active_user`
- `GET /db-demo` — yield dependency that opens & closes a fake "connection"
