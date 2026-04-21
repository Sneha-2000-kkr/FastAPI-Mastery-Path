"""OpenTelemetry setup. Optional — guarded so the app runs without OTel deps."""
from __future__ import annotations

import logging

from fastapi import FastAPI

log = logging.getLogger(__name__)


def setup_tracing(app: FastAPI, *, service_name: str, otlp_endpoint: str | None = None) -> None:
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.sdk.resources import SERVICE_NAME, Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import (
            BatchSpanProcessor,
            ConsoleSpanExporter,
        )
    except ImportError:
        log.warning("opentelemetry packages not installed — tracing disabled")
        return

    provider = TracerProvider(resource=Resource.create({SERVICE_NAME: service_name}))
    if otlp_endpoint:
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint)))
    else:
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app)
    log.info("tracing enabled", extra={"ctx_endpoint": otlp_endpoint or "console"})
