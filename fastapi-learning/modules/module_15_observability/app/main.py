from fastapi import FastAPI

from app.core.config import get_settings
from app.core.log import configure_logging
from app.core.middleware import ObservabilityMiddleware
from app.core.tracing import setup_tracing
from app.routes import work


def create_app() -> FastAPI:
    s = get_settings()
    configure_logging("INFO")
    app = FastAPI(title=s.app_name, version=s.version)
    app.add_middleware(ObservabilityMiddleware)
    if s.enable_tracing:
        setup_tracing(app, service_name=s.app_name, otlp_endpoint=s.otlp_endpoint)
    app.include_router(work.router)
    return app


app = create_app()
