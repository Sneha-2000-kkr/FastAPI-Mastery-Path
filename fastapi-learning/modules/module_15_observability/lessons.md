# Lesson 15 — Observability: Logging, Metrics, Tracing

## 1. Concept Deep Dive

The **three pillars**:
1. **Logs** — discrete events. Best for debugging individual requests.
2. **Metrics** — aggregated numbers over time. Best for SLOs, dashboards, alerts.
3. **Traces** — causal chains across services. Best for understanding distributed latency.

You need all three. Logs alone don't scale (you can't grep 1B lines/day). Metrics alone don't tell you *why*. Traces alone are expensive.

### Logging
- **Structured** (JSON), not free text. Every line is a queryable event.
- **Correlate** via a `request_id` (and `trace_id` if tracing). Use a `contextvars.ContextVar` so the id propagates across `await` without explicit passing.
- **Levels**: DEBUG (dev), INFO (events), WARNING (recoverable), ERROR (handled exception), CRITICAL (alarm).

### Metrics (Prometheus)
- **Counter** — monotonically increases. `requests_total{route, method, status}`.
- **Gauge** — current value. `inflight_requests`.
- **Histogram** — distribution. `request_duration_seconds_bucket`. The standard for latency.
- **Summary** — quantiles computed client-side (rarely the right choice; aggregation is hard).

Cardinality matters: *never* label with user-id or path-with-id. Use route templates (`/users/{id}`) not actual paths.

### Tracing (OpenTelemetry)
A **span** = a unit of work with start/end timestamps, attributes, and a parent. A **trace** = a tree of spans across services. Spans propagate via the `traceparent` HTTP header (W3C Trace Context).

OpenTelemetry has:
- **SDK** (in your app)
- **Instrumentations** (auto-patches frameworks/clients)
- **Exporter** (OTLP → Jaeger / Tempo / vendor)

## 2. Production Code Walkthrough

- `core/log.py` — JSON formatter; injects `request_id` from contextvar.
- `core/middleware.py` — assigns `request_id`, binds it to the contextvar, also feeds Prometheus + log line per request.
- `core/metrics.py` — Prometheus collectors + `/metrics` endpoint via `prometheus_client.generate_latest`.
- `core/tracing.py` — sets up OpenTelemetry with a console exporter (swap for OTLP).
- `routes/work.py` — endpoint that does fake work and emits log + custom span.

## 3. Why This Matters

You can't fix what you can't see. Observability is what turns 4-hour incidents into 4-minute ones.

## 4. Common Mistakes

- **High-cardinality metric labels** (user-id, full URL). Cardinality explodes, Prometheus dies.
- **Logging entire request bodies.** PII / secrets leak.
- **Different timestamp formats** across services. Use ISO-8601 UTC everywhere.
- **No sampling on traces** in high-RPS systems. Sample at 1–10%, plus head-based or tail-based for errors.
- **Treating health and readiness as the same.** `liveness` = "am I alive?" `readiness` = "should I receive traffic?"
- **Logging at INFO inside hot loops.** Disk I/O becomes the bottleneck.

## 5. Senior-Level Insights

- **Bind once, log many** — use a logger adapter that automatically injects `request_id`, `tenant_id`, `user_id`.
- **RED method** for service metrics: **R**ate, **E**rrors, **D**uration.
- **USE method** for resource metrics: **U**tilization, **S**aturation, **E**rrors.
- For traces, propagate context across **Celery / Kafka** too — otherwise your trace tree breaks at async boundaries. The OTel propagators ship with helpers.
- **SLOs > thresholds.** Define "99.9% of /checkout requests under 300ms over 30 days" and alert on **error budget burn rate**, not raw 5xx counts.
- **Logs as cheap traces**: if budget is tight, skip OTel and emit one `request.completed` log per request with `duration_ms`, `route`, `status`. Aggregate in Loki or similar.

## 6. Hands-on Task

Add a custom Prometheus counter `cache_hits_total` and increment it from a fake cache lookup in `/work`.

## 7. Mini Project

Replace the console span exporter with the OTLP HTTP exporter to Jaeger (`http://localhost:4318/v1/traces`) and visualise a trace across two endpoints (one calls the other via httpx with auto-instrumentation).
