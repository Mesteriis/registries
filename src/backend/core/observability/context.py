from contextvars import ContextVar, Token
from uuid import uuid4

_CORRELATION_ID: ContextVar[str | None] = ContextVar("correlation_id", default=None)
_REQUEST_ID: ContextVar[str | None] = ContextVar("request_id", default=None)


def generate_request_id() -> str:
    """Generate a new request identifier for an incoming HTTP request."""
    return uuid4().hex


def get_request_id() -> str | None:
    """Return the current request identifier from the active context."""
    return _REQUEST_ID.get()


def get_correlation_id() -> str | None:
    """Return the current correlation identifier from the active context."""
    return _CORRELATION_ID.get()


def set_request_id(request_id: str) -> Token[str | None]:
    """Bind a request identifier to the current execution context."""
    return _REQUEST_ID.set(request_id)


def set_correlation_id(correlation_id: str) -> Token[str | None]:
    """Bind a correlation identifier to the current execution context."""
    return _CORRELATION_ID.set(correlation_id)


def reset_request_id(token: Token[str | None]) -> None:
    """Reset the request identifier context to its previous value."""
    _REQUEST_ID.reset(token)


def reset_correlation_id(token: Token[str | None]) -> None:
    """Reset the correlation identifier context to its previous value."""
    _CORRELATION_ID.reset(token)
