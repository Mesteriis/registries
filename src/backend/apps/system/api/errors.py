from typing import Any

from core.errors import ResourceNotFoundError
from core.http.errors import ApiError, ApiErrorFactory
from fastapi import HTTPException, status

_ERROR_DESCRIPTIONS: dict[int, str] = {
    status.HTTP_404_NOT_FOUND: "Requested system resource was not found.",
    status.HTTP_500_INTERNAL_SERVER_ERROR: "Unexpected system error.",
}


def system_error_responses(*status_codes: int) -> dict[int | str, dict[str, Any]]:
    return {
        int(status_code): {
            "model": ApiError,
            "description": _ERROR_DESCRIPTIONS[int(status_code)],
        }
        for status_code in status_codes
    }


def system_resource_not_found_error(*, resource: str) -> HTTPException:
    return ApiErrorFactory.from_platform_error(ResourceNotFoundError(resource=resource))


__all__ = ["system_error_responses", "system_resource_not_found_error"]
