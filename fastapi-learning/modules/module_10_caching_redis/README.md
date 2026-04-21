# Module 10 — Caching with Redis

A `/quotes/{symbol}` endpoint that hits an upstream "stock API" (faked) and
caches the result in Redis with TTL + cache-aside pattern.

## Run
```bash
docker compose -f ../../docker/docker-compose.yml up -d redis
export APP_REDIS_URL=redis://localhost:6379/0
uvicorn app.main:app --reload --port 8000
```
