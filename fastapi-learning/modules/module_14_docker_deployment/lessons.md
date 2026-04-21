# Lesson 14 — Docker & Deployment

## 1. Concept Deep Dive

### Process model
For Python ASGI apps, the canonical production setup is:
- **Gunicorn** (process manager) + **UvicornWorker** (ASGI worker class)
- N workers = `2 * cpu_count + 1` for I/O-heavy, `cpu_count` for CPU-heavy
- Each worker has its own event loop
- A **reverse proxy** (Nginx, Caddy, ALB) terminates TLS, handles HTTP/2, gzip, and serves static assets

### Container basics
A good Dockerfile is:
1. **Multi-stage** — builder installs deps; runtime stage copies only what's needed.
2. **Layer-cached** — `COPY requirements.txt` before `COPY .` so dep install is cached when source changes.
3. **Non-root** — `USER appuser` with `1000:1000`.
4. **Pinned base** — `python:3.11.10-slim-bookworm`, not `:latest`.
5. **Has a HEALTHCHECK** — orchestrators use it to gate traffic.
6. **Small** — slim or distroless base, `--no-install-recommends`, clean apt lists.

### Signals & graceful shutdown
- Container PID 1 receives `SIGTERM` from the orchestrator.
- Gunicorn forwards it; workers finish in-flight requests then exit.
- Set `--graceful-timeout 30` (Gunicorn) and `terminationGracePeriodSeconds: 60` (k8s) so long requests don't get cut off.
- FastAPI's lifespan `finally` block runs on shutdown — close DB pools, flush logs.

### Zero-downtime deploys
Rolling deploys + readiness probes. The new pod's `/healthz` must return 200 *and* report dependencies (DB, Redis) as healthy before it gets traffic.

## 2. Production Code Walkthrough

- `deploy/Dockerfile` — multi-stage build, slim base, non-root, healthcheck.
- `deploy/docker-compose.yml` — runs the app + Postgres for end-to-end local dev.
- `gunicorn/gunicorn_conf.py` — workers, timeouts, log format.
- `app/main.py` — adds `/healthz` and `/readyz`.

## 3. Why This Matters

Container hygiene + signals are the difference between deploys that "just work" and 3am Slack pages. The patterns here are what every k8s-based shop expects.

## 4. Common Mistakes

- **Using `python:3.11` (not `-slim`)** → 1 GB image. Slim is ~120 MB.
- **`COPY . .` then `pip install`** — every code change re-installs deps.
- **Running as root** in the container.
- **No healthcheck** → orchestrator routes traffic to a broken process.
- **`--reload` in production**. It exists only for dev.
- **Ignoring `SIGTERM`** → orchestrator sends `SIGKILL` after the grace period and you lose in-flight work.

## 5. Senior-Level Insights

- For minimal attack surface, switch to a **distroless** runtime (`gcr.io/distroless/python3-debian12`). No shell, fewer CVEs.
- **Bake the version** into the image as a label and an env var so `/healthz` can return it.
- **Multi-arch builds** (`docker buildx --platform linux/amd64,linux/arm64`) for Apple Silicon devs + amd64 prod.
- Set Gunicorn `--worker-tmp-dir /dev/shm` to avoid disk-IO heartbeat waits in containers (a classic k8s gotcha).
- Mount `/var/log` and `/tmp` as `tmpfs` and run the FS read-only (`--read-only`) for hardening.
- For autoscaling, expose **CPU + queue depth** metrics; HPA on CPU alone is rarely the right signal for I/O-bound APIs.

## 6. Hands-on Task

Add a multi-stage Dockerfile that uses `pip install --user` in the builder, then copies `~/.local` into a `python:3.11-slim` runtime — shrinks image further.

## 7. Mini Project

Add `docker-bake.hcl` with a `release` target that builds `linux/amd64` + `linux/arm64`, tags `:latest` and `:${VERSION}`, and pushes to a registry.
