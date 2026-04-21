"""Domain-level exceptions — translated to HTTP at the edge."""


class DomainError(Exception):
    code: str = "domain_error"
    http_status: int = 400


class NotFoundError(DomainError):
    code = "not_found"
    http_status = 404


class ConflictError(DomainError):
    code = "conflict"
    http_status = 409


class CustomerNotFound(NotFoundError):
    pass


class OrderNotFound(NotFoundError):
    pass


class InsufficientStock(ConflictError):
    code = "insufficient_stock"
