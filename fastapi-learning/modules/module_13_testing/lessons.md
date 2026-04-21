# Lesson 13 — Testing FastAPI Apps

## 1. Concept Deep Dive

A FastAPI app is testable on three levels:
1. **Unit** — services and pure functions, no app at all. Fastest, easiest. Aim for the most coverage here.
2. **API** — start the app in-process, hit it with a client. Use `httpx.AsyncClient(transport=ASGITransport(app=app))`. No network, no port — fast and deterministic.
3. **Integration / E2E** — real DB (Testcontainers), real Redis, real network. Slower; reserve for smoke tests.

### Test client choice
- `TestClient` (Starlette) — sync, runs the app on a background loop. Easy. Default for many tutorials.
- `httpx.AsyncClient` + `ASGITransport` — async-native. Required if your tests are `async def` and want to share an event loop.

### Fixtures
- `pytest-asyncio` adds `@pytest.mark.asyncio` and the `event_loop` fixture.
- Build `app` per test (or per module) so dependency overrides don't bleed between tests.
- Use `app.dependency_overrides[real] = fake` and clear in teardown.

### What to test
- **Happy paths** for every endpoint.
- **Validation failures** — Pydantic 422.
- **Domain failures** — 404/409/etc.
- **Auth boundaries** — 401 / 403.
- **Idempotency / cursors / ETags** — easy to break, easy to test.

## 2. Production Code Walkthrough

- `app/...` — minimal `/items` app like module 01.
- `tests/conftest.py` — fixtures: `app`, `async_client`. Uses `httpx.AsyncClient` with `ASGITransport`.
- `tests/test_items_api.py` — API-level tests of CRUD.
- `tests/test_item_service.py` — pure unit tests with a fake repo.

## 3. Why This Matters

Untested code rots. A small but **trustworthy** test suite is more valuable than a huge one nobody trusts. The patterns here scale.

## 4. Common Mistakes

- **Sharing app/client state across tests.** Cleanup `dependency_overrides` always.
- **Hitting real external services in CI.** Mock at the boundary; have a separate "integration" suite gated by an env var.
- **Testing through the HTTP layer when a unit test would do.** Slow and harder to debug.
- **Snapshot tests on JSON.** They fail on every refactor. Test invariants, not exact bytes.
- **Forgetting to seed clean DB state** between tests. Use transactions per test (rollback at end) or fresh schemas.

## 5. Senior-Level Insights

- **Test pyramid**: lots of unit, fewer API, very few E2E. Inverting it makes CI slow and flaky.
- For DB tests, **start a transaction per test and roll back** — orders of magnitude faster than recreating schemas.
- For real Postgres in CI, use **Testcontainers** to spin a clean instance per job.
- Use **httpx parametrize** for table-driven tests — many cases, one assertion.
- Mark slow tests with `@pytest.mark.slow` and exclude them from default `pytest` runs (`pytest -m "not slow"`).
- Aim for fast feedback (<10s) on the unit suite. If pytest takes 5 minutes, devs stop running it.

## 6. Hands-on Task

Add a parametrized test that POSTs invalid payloads (missing field, negative price, oversized name) and asserts 422 with the right `loc` path.

## 7. Mini Project

Add a `pytest-postgresql` (or Testcontainers) integration suite for the module 05 app: real Postgres, real session, transaction-per-test rollback.
