# Module 02 — Pydantic v2 Deep Dive

Validation, serialization, validators, custom types, discriminated unions,
field aliases, model composition, and the new `Annotated` pattern.

Endpoints:
- `POST /users` — create user, demonstrates email + password rules + computed fields
- `POST /products` — discriminated union (book vs electronic)
- `GET  /products` — serialization aliases (`camelCase` over the wire, `snake_case` in Python)

## Run
```bash
uvicorn app.main:app --reload --port 8000
```
