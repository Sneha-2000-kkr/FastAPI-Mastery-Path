# Module 05 — PostgreSQL + SQLAlchemy 2.0 (Async)

A real, persistent `/items` resource using async SQLAlchemy + asyncpg.

## Run

```bash
docker compose -f ../../docker/docker-compose.yml up -d postgres
export APP_DATABASE_URL=postgresql+asyncpg://fapi:fapi@localhost:5432/fapi
uvicorn app.main:app --reload --port 8000
```

Tables are auto-created on startup (for learning). In production use Alembic — see `alembic/` stub and the lesson.
