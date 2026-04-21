# Module 15 — Observability (logs, metrics, tracing)

Three pillars stitched together:
- **Structured JSON logging** with request-id correlation (contextvar).
- **Prometheus metrics** at `/metrics` (request count, latency histogram, in-progress gauge).
- **OpenTelemetry tracing** (auto-instrumented FastAPI; exports to OTLP/console).

Endpoints:
- `GET /work?ms=200`
- `GET /metrics`
- `GET /healthz`

## Run
```bash
uvicorn app.main:app --reload --port 8000
curl http://localhost:8000/work?ms=120
curl http://localhost:8000/metrics
```
