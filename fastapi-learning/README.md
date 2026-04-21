# FastAPI Learning — A Production-Grade Backend Course

A hands-on, module-by-module FastAPI learning repository. Each module is a **runnable mini-project** that builds on the previous one, evolving from basic routing into a production-shaped backend system covering databases, auth, async, caching, background jobs, testing, deployment, and observability.

This is **not** a tutorial of toy snippets. Every module ships a layered codebase (`routes → services → repository → models`), real configuration, error handling, and an in-depth `lessons.md` covering internals, common production mistakes, and senior-level trade-offs.

## Modules

| # | Topic |
|---|-------|
| 01 | FastAPI Basics — routing, request lifecycle |
| 02 | Pydantic Deep Dive — request/response models |
| 03 | Dependency Injection — internals & patterns |
| 04 | Project Structuring — layered/clean architecture |
| 05 | PostgreSQL + SQLAlchemy 2.0 (async) |
| 06 | MongoDB (Motor, async ODM patterns) |
| 07 | Authentication — JWT + OAuth2 password flow |
| 08 | Middleware & Exception Handling |
| 09 | Async Programming Deep Dive |
| 10 | Caching with Redis |
| 11 | Background Jobs (Celery / RQ) |
| 12 | API Design Best Practices (versioning, pagination, idempotency) |
| 13 | Testing (pytest + httpx + integration tests) |
| 14 | Docker & Deployment |
| 15 | Observability (logging, metrics, tracing) |

## Running a Module

Each module is independently runnable:

```bash
cd modules/module_01_basics
pip install -r ../../requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

## Repo Layout

```
fastapi-learning/
├── modules/
│   ├── module_01_basics/
│   │   ├── lessons.md
│   │   ├── README.md
│   │   └── app/
│   │       ├── main.py
│   │       ├── core/
│   │       ├── routes/
│   │       ├── schemas/
│   │       ├── models/
│   │       ├── services/
│   │       ├── repository/
│   │       └── dependencies/
│   └── ...
├── shared/        # cross-module utilities
├── docker/        # docker-compose stacks for postgres, redis, mongo
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.11+
- Docker (for modules 05, 06, 10, 11, 14)
- A code editor with Python LSP

## How to Use This Repo

Read `lessons.md` first, then walk the code in this order: `core/config.py → main.py → routes/ → services/ → repository/ → models/ → schemas/`. Run the app, hit the endpoints in `/docs`, then attempt the **Hands-on Task** at the end of each lesson.
