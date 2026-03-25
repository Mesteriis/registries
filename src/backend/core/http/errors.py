from collections.abc import Mapping

from fastapi import HTTPException
from pydantic import BaseModel, Field

from core.errors import PlatformError


class ApiErrorDetail(BaseModel):
    field: str | None = None
    message: str
    value: object | None = None


class ApiError(BaseModel):
    code: str
    message: str
    message_key: str | None = None
    domain: str | None = None
    category: str | None = None
    http_status: int | None = None
    severity: str | None = None
    safe_to_expose: bool | None = None
    details: tuple[ApiErrorDetail, ...] = Field(default_factory=tuple)
    retryable: bool = False
    request_id: str | None = None
    correlation_id: str | None = None


class ApiErrorFactory:
    @staticmethod
    def build_detail(
        *,
        message: str,
        field: str | None = None,
        value: object | None = None,
    ) -> ApiErrorDetail:
        return ApiErrorDetail(field=field, message=message, value=value)

    @staticmethod
    def build(
        *,
        code: str,
        message: str,
        message_key: str | None = None,
        domain: str | None = None,
        category: str | None = None,
        http_status: int | None = None,
        severity: str | None = None,
        safe_to_expose: bool | None = None,
        details: tuple[ApiErrorDetail, ...] = (),
        retryable: bool = False,
        request_id: str | None = None,
        correlation_id: str | None = None,
    ) -> ApiError:
        return ApiError(
            code=code,
            message=message,
            message_key=message_key,
            domain=domain,
            category=category,
            http_status=http_status,
            severity=severity,
            safe_to_expose=safe_to_expose,
            details=details,
            retryable=retryable,
            request_id=request_id,
            correlation_id=correlation_id,
        )

    @staticmethod
    def build_from_platform_error(
        exc: PlatformError,
        *,
        details: tuple[ApiErrorDetail, ...] = (),
        request_id: str | None = None,
        correlation_id: str | None = None,
    ) -> ApiError:
        return ApiErrorFactory.build(
            code=exc.code,
            message=exc.message,
            message_key=exc.message_key,
            domain=exc.domain.value,
            category=exc.category.value,
            http_status=exc.http_status,
            severity=exc.severity.value,
            safe_to_expose=exc.safe_to_expose,
            details=details,
            retryable=exc.retryable,
            request_id=request_id,
            correlation_id=correlation_id,
        )

    @staticmethod
    def from_platform_error(
        exc: PlatformError,
        *,
        details: tuple[ApiErrorDetail, ...] = (),
        request_id: str | None = None,
        correlation_id: str | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> HTTPException:
        payload = ApiErrorFactory.build_from_platform_error(
            exc,
            details=details,
            request_id=request_id,
            correlation_id=correlation_id,
        )
        return HTTPException(
            status_code=exc.http_status,
            detail=payload.model_dump(mode="json"),
            headers=dict(headers or {}),
        )


__all__ = ["ApiError", "ApiErrorDetail", "ApiErrorFactory"]
