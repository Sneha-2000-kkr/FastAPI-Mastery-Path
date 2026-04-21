# Module 06 — MongoDB (Motor, async)

`/articles` CRUD against MongoDB using Motor.

## Run
```bash
docker compose -f ../../docker/docker-compose.yml up -d mongo
export APP_MONGO_URL=mongodb://localhost:27017
uvicorn app.main:app --reload --port 8000
```
