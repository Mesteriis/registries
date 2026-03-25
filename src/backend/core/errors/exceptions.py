from collections.abc import Mapping

from core.errors.catalog import PLATFORM_ERROR_REGISTRY
from core.errors.registry import ErrorDefinition


class PlatformError(Exception):
    def __init__(
        self,
        definition: ErrorDefinition,
        *,
        params: Mapping[str, object] | None = None,
        details: Mapping[str, object] | None = None,
        retryable: bool | None = None,
    ) -> None:
        self.definition = definition
        self.params = dict(params or {})
        self.details = dict(details or {})
        self.code = definition.error_code
        self.message_key = definition.message_key
        self.message = definition.render_message(self.params)
        self.http_status = definition.http_status
        self.domain = definition.domain
        self.category = definition.category
        self.severity = definition.severity
        self.retryable = definition.retryable if retryable is None else retryable
        self.safe_to_expose = definition.safe_to_expose
        super().__init__(self.message)

    def to_metadata(self) -> dict[str, object]:
        return {
            "error_code": self.code,
            "message_key": self.message_key,
            "domain": self.domain.value,
            "category": self.category.value,
            "http_status": self.http_status,
            "severity": self.severity.value,
            "retryable": self.retryable,
            "safe_to_expose": self.safe_to_expose,
            "params": dict(self.params),
            "details": dict(self.details),
        }


class RegistryBackedPlatformError(PlatformError):
    error_code: str

    def __init__(
        self,
        *,
        details: Mapping[str, object] | None = None,
        params: Mapping[str, object] | None = None,
        retryable: bool | None = None,
    ) -> None:
        super().__init__(
            PLATFORM_ERROR_REGISTRY.get(self.error_code),
            details=details,
            params=params,
            retryable=retryable,
        )


class InternalPlatformError(RegistryBackedPlatformError):
    error_code = "internal_error"


class ValidationFailedError(RegistryBackedPlatformError):
    error_code = "validation_failed"


class ResourceNotFoundError(RegistryBackedPlatformError):
    error_code = "resource_not_found"

    def __init__(
        self,
        *,
        resource: str,
        details: Mapping[str, object] | None = None,
    ) -> None:
        super().__init__(details=details, params={"resource": resource})


class DuplicateRequestError(RegistryBackedPlatformError):
    error_code = "duplicate_request"


class IntegrationUnreachableError(RegistryBackedPlatformError):
    error_code = "integration_unreachable"

    def __init__(
        self,
        *,
        integration: str,
        details: Mapping[str, object] | None = None,
        retryable: bool | None = None,
    ) -> None:
        super().__init__(
            details=details,
            params={"integration": integration},
            retryable=retryable,
        )


__all__ = [
    "DuplicateRequestError",
    "IntegrationUnreachableError",
    "InternalPlatformError",
    "PlatformError",
    "RegistryBackedPlatformError",
    "ResourceNotFoundError",
    "ValidationFailedError",
]
