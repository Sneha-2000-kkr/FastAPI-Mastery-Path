import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

log = logging.getLogger(__name__)


class DomainError(Exception):
    code: str = "domain_error"
    http_status: int = 400


class NotFound(DomainError):
    code, http_status = "not_found", 404


class Conflict(DomainError):
    code, http_status = "conflict", 409


def _envelope(*, code: str, message: str, request: Request, details=None, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "details": details,
                "request_id": getattr(request.state, "request_id", None),
            }
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def _domain(request: Request, exc: DomainError):
        return _envelope(code=exc.code, message=str(exc) or exc.code,
                         request=request, status_code=exc.http_status)

    @app.exception_handler(StarletteHTTPException)
    async def _http(request: Request, exc: StarletteHTTPException):
        return _envelope(code="http_error", message=str(exc.detail),
                         request=request, status_code=exc.status_code)

    @app.exception_handler(RequestValidationError)
    async def _validation(request: Request, exc: RequestValidationError):
        return _envelope(code="validation_error", message="invalid request",
                         request=request, details={"errors": exc.errors()},
                         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception):
        log.exception("unhandled exception")
        return _envelope(code="internal_error", message="internal server error",
                         request=request, status_code=500)
