# Module 07 — Authentication (JWT + OAuth2 password flow)

`/auth/register`, `/auth/token` (OAuth2 password grant), `/me`, `/admin` (role-protected).

## Run
```bash
export APP_JWT_SECRET=$(python -c "import secrets;print(secrets.token_hex(32))")
uvicorn app.main:app --reload --port 8000
```
