# Module 01 — FastAPI Basics

A minimal but production-shaped FastAPI app exposing a `/items` resource.
We focus on the **request lifecycle**: how Starlette receives an HTTP request,
how FastAPI resolves the route + dependencies, validates input via Pydantic,
runs your handler, serializes the response, and writes it back.

## Run

```bash
pip install -r ../../requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000/docs`.

## Endpoints

- `GET  /healthz`
- `GET  /items?limit=10&offset=0`
- `GET  /items/{item_id}`
- `POST /items`
- `DELETE /items/{item_id}`
