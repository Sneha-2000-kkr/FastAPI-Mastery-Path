# Module 11 — Background Jobs (Celery & RQ)

Two patterns:
1. `BackgroundTasks` (FastAPI built-in) for tiny same-process tasks.
2. **Celery** (with Redis broker) for real distributed work.
3. **RQ** as a simpler alternative.

Endpoints:
- `POST /jobs/email`           — enqueues a Celery task; returns task id
- `GET  /jobs/{task_id}`       — checks task status
- `POST /jobs/report`          — enqueues an RQ task
- `POST /notify`               — same-process via `BackgroundTasks`

## Run
```bash
docker compose -f ../../docker/docker-compose.yml up -d redis
export APP_REDIS_URL=redis://localhost:6379/0
# Terminal 1: API
uvicorn app.main:app --reload --port 8000
# Terminal 2: Celery worker
celery -A app.workers.celery_app worker --loglevel=INFO
# Terminal 3 (optional): RQ worker
rq worker --url redis://localhost:6379/0 reports
```
