import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.log import request_id_var
from app.core.metrics import INFLIGHT, LATENCY, REQUESTS

log = logging.getLogger("http")


def _route_template(request: Request) -> str:
    route = request.scope.get("route")
    return getattr(route, "path", request.url.path)


class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        token = request_id_var.set(rid)
        request.state.request_id = rid

        method = request.method
        # Path is best-effort here; the matched route template is set after routing.
        # We finalise after call_next so we use the templated path for labels.
        t0 = time.perf_counter()

        # Pre-increment inflight on the raw path (acceptable; cleaned post-call).
        path_pre = request.url.path
        INFLIGHT.labels(method, path_pre).inc()
        try:
            response = await call_next(request)
        finally:
            INFLIGHT.labels(method, path_pre).dec()
            request_id_var.reset(token)

        dt = time.perf_counter() - t0
        route = _route_template(request)
        REQUESTS.labels(method, route, str(response.status_code)).inc()
        LATENCY.labels(method, route).observe(dt)
        response.headers["X-Request-ID"] = rid
        log.info(
            "request.completed",
            extra={
                "ctx_method": method,
                "ctx_route": route,
                "ctx_status": response.status_code,
                "ctx_duration_ms": round(dt * 1000, 2),
            },
        )
        return response
