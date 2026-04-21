# Module 12 — API Design Best Practices

Demonstrates URI versioning (`/v1`), cursor pagination, idempotency keys,
ETag + conditional requests, and HATEOAS-lite hypermedia.

Endpoints under `/v1/posts`:
- `GET /v1/posts?cursor=...&limit=...`
- `GET /v1/posts/{id}` with `ETag` and `If-None-Match`
- `POST /v1/posts` with `Idempotency-Key` header
- `PATCH /v1/posts/{id}` with `If-Match` (optimistic concurrency)
