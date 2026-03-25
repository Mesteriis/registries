from typing import cast

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from core.errors import InternalPlatformError, PlatformError, ValidationFailedError
from core.http.errors import ApiErrorDetail, ApiErrorFactory
from core.observability import capture_handled_exception, get_logger
from core.observability.context import get_correlation_id, get_request_id

HTTP_ERROR_LOGGER = get_logger("core.http.handlers")


def _field_name(parts: tuple[object, ...]) -> str:
    return ".".join(str(part) for part in parts)


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
            field=_field_name(tuple(error.get("loc", ()))),
            message=str(error.get("msg", "Validation failed.")),
            value=error.get("input"),
        )
        for error in validation_error.errors()
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
