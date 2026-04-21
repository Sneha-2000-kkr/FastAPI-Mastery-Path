# Module 14 — Docker & Deployment

A production-grade Dockerfile (multi-stage, non-root, healthcheck) plus
`docker-compose.yml` for the full app, gunicorn config, and notes on rolling
deploys / zero-downtime.

## Build & run

```bash
docker build -t fapi-app:latest -f deploy/Dockerfile .
docker run --rm -p 8000:8000 fapi-app:latest
# or:
docker compose -f deploy/docker-compose.yml up --build
```

The app itself is the same `/items` API as module 01 — focus is on the
deployment artifacts.
