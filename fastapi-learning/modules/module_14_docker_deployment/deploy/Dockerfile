# syntax=docker/dockerfile:1.7

# ---- builder ----------------------------------------------------------------
FROM python:3.11.10-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

RUN apt-get update \
 && apt-get install --no-install-recommends -y build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY ../../requirements.txt /tmp/requirements.txt
RUN pip install --user -r /tmp/requirements.txt gunicorn==23.0.0

# ---- runtime ----------------------------------------------------------------
FROM python:3.11.10-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}" \
    PORT=8000

RUN groupadd --system --gid 1000 app \
 && useradd  --system --uid 1000 --gid 1000 --create-home appuser

WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local
COPY app /app/app
COPY gunicorn/gunicorn_conf.py /app/gunicorn_conf.py

RUN chown -R appuser:app /app /home/appuser/.local
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request,sys;\
sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2).status==200 else 1)"

CMD ["gunicorn", "-c", "/app/gunicorn_conf.py", "app.main:app"]
