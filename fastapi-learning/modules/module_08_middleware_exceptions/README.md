# Module 08 — Middleware & Exception Handling

Custom middlewares (request id, timing, body-size limit), centralized exception
handlers, and a uniform error envelope.

Endpoints:
- `GET /ping` — fast
- `GET /slow` — sleeps 1.5s
- `GET /boom` — raises a custom domain error
- `POST /echo` — echoes JSON; tests body-size middleware
