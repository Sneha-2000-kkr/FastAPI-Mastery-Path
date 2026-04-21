# Lesson 07 — Authentication (JWT + OAuth2 password)

## 1. Concept Deep Dive

### OAuth2 Password Flow (RFC 6749 §4.3)
The client sends `username` + `password` as **form-encoded** data to the token endpoint, and gets back `{access_token, token_type, expires_in}`. This is what FastAPI's `OAuth2PasswordRequestForm` parses. It's appropriate for **first-party** clients only — never expose it to third-party apps.

### JWT (RFC 7519)
A JWT is `base64url(header) . base64url(payload) . base64url(signature)`. It is **signed**, not encrypted — anyone with the token can read its claims. Standard claims:
- `sub` — subject (user id)
- `iat` — issued at
- `exp` — expiry
- `iss` / `aud` — issuer / audience (validate them!)

### Algorithm choice
- **HS256** uses a shared secret. Fine for a single-service backend.
- **RS256** uses a private/public keypair. Use it when multiple services need to verify tokens; only the auth service holds the private key.
- Never accept the `alg: none` token. Modern libraries reject it by default; old ones did not (CVE history).

### Password hashing
Use **bcrypt** (or argon2). Never SHA. `passlib` provides the canonical interface; the cost factor is tunable.

## 2. Production Code Walkthrough

- `core/security.py` — `hash_password`, `verify_password`, `create_access_token`, `decode_token`. PyJWT under the hood.
- `core/config.py` — `JWT_SECRET`, `JWT_ALG`, `JWT_EXPIRES_MIN`, `JWT_ISSUER`, `JWT_AUDIENCE`.
- `models/user.py` + `repository/user_repository.py` — in-memory users with `password_hash` and `roles`.
- `services/auth_service.py` — `register`, `authenticate`. Constant-time compare on missing user via dummy hash to prevent user enumeration timing attacks.
- `dependencies/auth.py` — `get_current_user` parses `Authorization: Bearer ...`; `require_role(role)` returns a dependency.
- `routes/auth.py`, `routes/me.py`, `routes/admin.py`.

## 3. Why This Matters

Auth bugs are the most common source of production breaches. Stateless JWTs scale (no session store) but are hard to revoke — so you must keep `exp` short and pair them with refresh tokens or a denylist for high-value sessions.

## 4. Common Mistakes

- **Long-lived tokens.** 24h JWTs that can't be revoked = a stolen token = full account access for a day.
- **Trusting the `alg` header.** Always pass `algorithms=[...]` to `jwt.decode`. Otherwise an attacker can flip RS256 → HS256 and use the public key as the secret.
- **Logging tokens.** Treat them like passwords.
- **Using `password.lower() == ...` style comparisons.** Use bcrypt's `verify`, which is constant-time.
- **Not validating `aud` / `iss`.** A token issued for service A should not be accepted by service B.
- **Storing JWTs in localStorage.** XSS vulnerable. Prefer httpOnly cookies, accepting CSRF mitigations.

## 5. Senior-Level Insights

- Pair short-lived **access tokens** (5–15 min) with longer **refresh tokens** stored server-side (rotated on use). On refresh-token theft, rotate detection invalidates the family.
- Add `jti` (JWT ID) to every token; persist a denylist of revoked `jti`s with TTL = remaining `exp`. Cheap revocation.
- For B2B/SSO, prefer **OIDC** (OpenID Connect) on top of OAuth2 — it standardises the user info claim.
- For mobile, use **PKCE** + the device authorization grant; never the password grant.
- Migrate hashes lazily: on successful login, if `password_hash` is the old algorithm, rehash and persist.

## 6. Hands-on Task

Add `/auth/refresh` returning a new access token. Track `jti` in memory and reject reused refresh tokens.

## 7. Mini Project

Add role-based access: `Depends(require_role("admin"))`. Create `/admin/users` listing users (admin only). Seed an admin user at startup.
