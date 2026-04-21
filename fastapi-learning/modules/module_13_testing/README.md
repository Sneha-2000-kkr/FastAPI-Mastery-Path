# Module 13 — Testing (pytest + httpx + dependency overrides)

A small `/items` app + a real test suite covering:
- unit tests for services
- API tests via `httpx.AsyncClient` and `ASGITransport`
- dependency overrides to swap repositories
- fixtures for app + client

## Run
```bash
pip install -r ../../requirements.txt
pytest -q
```
