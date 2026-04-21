from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from starlette.responses import Response

REQUESTS = Counter(
    "http_requests_total",
    "HTTP requests",
    labelnames=("method", "route", "status"),
)
LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    labelnames=("method", "route"),
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
)
INFLIGHT = Gauge(
    "http_requests_inflight",
    "In-flight HTTP requests",
    labelnames=("method", "route"),
)


def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
