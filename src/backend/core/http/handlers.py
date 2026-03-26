import math
from typing import cast

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from core.errors import InternalPlatformError, PlatformError, ValidationFailedError
from core.http.errors import ApiErrorDetail, ApiErrorFactory
from core.observability import capture_handled_exception, get_logger
from core.observability.context import get_correlation_id, get_request_id

HTTP_ERROR_LOGGER = get_logger("core.http.handlers")
_FILTERED_VALUE = "[FILTERED]"
_REDACTED_VALUE = "[REDACTED]"
_MAX_VALIDATION_VALUE_LENGTH = 120
_SENSITIVE_FIELD_PARTS = frozenset(
    {
        "authorization",
        "cookie",
        "credential",
        "credentials",
        "password",
        "secret",
        "set-cookie",
        "token",
    }
)


def _field_name(parts: tuple[object, ...]) -> str:
    return ".".join(str(part) for part in parts)


def _sanitize_validation_input(*, field: str | None, value: object | None) -> object | None:
    if value is None:
        return None

    if _is_sensitive_field(field):
        return _REDACTED_VALUE

    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return value

    if isinstance(value, float):
        return value if math.isfinite(value) else _FILTERED_VALUE

    if isinstance(value, str):
        return _truncate_validation_value(value)

    return _FILTERED_VALUE


def _is_sensitive_field(field: str | None) -> bool:
    if not field:
        return False

    field_parts = {part.lower() for part in field.split(".") if part}
    return not field_parts.isdisjoint(_SENSITIVE_FIELD_PARTS)


def _truncate_validation_value(value: str) -> str:
    if len(value) <= _MAX_VALIDATION_VALUE_LENGTH:
        return value

    return f"{value[:_MAX_VALIDATION_VALUE_LENGTH]}..."


def _resolved_request_id(request: Request) -> str | None:
    request_id = get_request_id()
    if request_id is not None:
        return request_id

    state_request_id = getattr(request.state, "request_id", None)
    return str(state_request_id) if state_request_id is not None else None


def _resolved_correlation_id(request: Request) -> str | None:
    correlation_id = get_correlation_id()
    if correlation_id is not None:
        return correlation_id

    state_correlation_id = getattr(request.state, "correlation_id", None)
    return str(state_correlation_id) if state_correlation_id is not None else None


def _context_headers(request: Request) -> dict[str, str]:
    headers: dict[str, str] = {}
    request_id = _resolved_request_id(request)
    if request_id is not None:
        request_id_header_name = getattr(request.app.state, "request_id_header", "X-Request-ID")
        headers[str(request_id_header_name)] = request_id

    correlation_id = _resolved_correlation_id(request)
    if correlation_id is not None:
        correlation_id_header_name = getattr(request.app.state, "correlation_id_header", "X-Correlation-ID")
        headers[str(correlation_id_header_name)] = correlation_id

    return headers


async def handle_platform_error(request: Request, exc: Exception) -> JSONResponse:
    platform_error = cast(PlatformError, exc)
    payload = ApiErrorFactory.build_from_platform_error(
        platform_error,
        request_id=_resolved_request_id(request),
        correlation_id=_resolved_correlation_id(request),
    )
    return JSONResponse(
        status_code=platform_error.http_status,
        content=payload.model_dump(mode="json"),
        headers=_context_headers(request),
    )


async def handle_request_validation_error(request: Request, exc: Exception) -> JSONResponse:
    validation_error = cast(RequestValidationError, exc)
    details: tuple[ApiErrorDetail, ...] = tuple(
        ApiErrorFactory.build_detail(
            field=field_name,
            message=str(error.get("msg", "Validation failed.")),
            value=_sanitize_validation_input(field=field_name, value=error.get("input")),
        )
        for error in validation_error.errors()
        for field_name in (_field_name(tuple(error.get("loc", ()))),)
    )
    platform_error = ValidationFailedError()
    payload = ApiErrorFactory.build_from_platform_error(
        platform_error,
        details=details,
        request_id=_resolved_request_id(request),
        correlation_id=_resolved_correlation_id(request),
    )
    return JSONResponse(
        status_code=platform_error.http_status,
        content=payload.model_dump(mode="json"),
        headers=_context_headers(request),
    )


async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    capture_handled_exception(request, exc)
    HTTP_ERROR_LOGGER.exception("Unhandled backend exception", path=request.url.path, method=request.method)
    platform_error = InternalPlatformError()
    payload = ApiErrorFactory.build_from_platform_error(
        platform_error,
        request_id=_resolved_request_id(request),
        correlation_id=_resolved_correlation_id(request),
    )
    return JSONResponse(
        status_code=platform_error.http_status,
        content=payload.model_dump(mode="json"),
        headers=_context_headers(request),
    )


__all__ = [
    "handle_platform_error",
    "handle_request_validation_error",
    "handle_unexpected_error",
]
