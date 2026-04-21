# Lesson 12 — API Design Best Practices

## 1. Concept Deep Dive

### Versioning
- **URI versioning** (`/v1/...`) is explicit and cache-friendly. Default choice.
- **Header versioning** (`Accept: application/vnd.app.v2+json`) is purer REST but less debuggable.
- **No versioning** is fine for internal APIs with one client. Public APIs need a story.

### Pagination
- **Offset/limit** is simple but breaks under concurrent inserts (skipped/duplicated rows) and is O(N) at deep offsets.
- **Cursor (keyset) pagination** uses `WHERE (created_at, id) < (last_seen_created_at, last_seen_id) ORDER BY created_at DESC, id DESC LIMIT n`. Stable under writes, O(log N) on indexed columns. Always prefer for unbounded lists.

### Idempotency
A `POST /payments` retried after a network blip must not charge twice. Convention: `Idempotency-Key: <uuid>` header. Server stores `(key → response)` for some TTL; replays return the cached response.

### Conditional requests
- `ETag` (entity tag) on responses → client sends `If-None-Match` on next read → 304 if unchanged.
- `If-Match` on writes → 412 if the resource has changed since the client read it (optimistic concurrency).

### Errors
Use **RFC 7807 Problem Details** (`application/problem+json`) or your own consistent envelope (module 08). The cardinal rule: same shape everywhere.

## 2. Production Code Walkthrough

- `routes/v1/posts.py` — uses cursor, ETags computed from a content hash, idempotency middleware via a `Header(...)` dep.
- `services/post_service.py` — domain logic.
- `services/idempotency.py` — in-memory store keyed by `(method, path, key)`.
- `core/etag.py` — strong ETag from canonical JSON.

## 3. Why This Matters

These patterns are the difference between an API a client team enjoys and one they merely tolerate. They also unlock proxies and CDNs (304 responses), prevent double-spends (idempotency), and let mobile clients sync efficiently (cursors).

## 4. Common Mistakes

- **Versioning per resource** (`/posts/v2`) — inconsistent, hard to evolve.
- **Storing pagination cursors as offsets in disguise** — same problem.
- **Not validating that `Idempotency-Key` matches the original request body.** Replays of *different* requests with the same key must return 422.
- **Weak ETags everywhere.** Use strong ETags (`"abc123"` not `W/"abc123"`) when the body is byte-identical for the same state.
- **Returning 200 with `{"error":...}`.** Use proper status codes.

## 5. Senior-Level Insights

- **Backwards compatibility**: never remove a field, never change a type, never tighten a constraint. Add new fields, deprecate old ones with `Sunset:` and `Deprecation:` headers, then remove in v(N+1).
- **Resource modeling**: model nouns, not RPCs. `POST /orders/{id}/cancel` is fine; `POST /cancelOrder` is not.
- **Pagination is a contract**. Document `limit` bounds, default sort, cursor opacity. Cursors should be opaque base64.
- **Rate limits** belong in the response (`X-RateLimit-Remaining`, `X-RateLimit-Reset`). Don't make clients guess.
- **Error catalogs**: every error code is documented with cause + remediation. Client devs love it.

## 6. Hands-on Task

Add a `Sunset: <date>` and `Deprecation: true` header to all `/v1/...` responses via a middleware once `/v2` ships.

## 7. Mini Project

Add `/v2/posts` that returns the same data with a renamed `body` → `content`. Provide a deprecation notice in `/v1` and a migration endpoint.
