from http import HTTPStatus

from core.errors.registry import ErrorDefinition, ErrorRegistry
from core.errors.taxonomy import ErrorCategory, ErrorDomain, ErrorSeverity

PLATFORM_ERROR_REGISTRY = ErrorRegistry(
    definitions=(
        ErrorDefinition(
            error_code="internal_error",
            message_key="error.system.internal",
            default_message="Internal server error.",
            domain=ErrorDomain.CORE,
            category=ErrorCategory.INTERNAL,
            http_status=int(HTTPStatus.INTERNAL_SERVER_ERROR),
            severity=ErrorSeverity.ERROR,
            retryable=False,
            safe_to_expose=False,
        ),
        ErrorDefinition(
            error_code="resource_not_found",
            message_key="error.resource.not_found",
            default_message="Requested {resource} was not found.",
            domain=ErrorDomain.API,
            category=ErrorCategory.NOT_FOUND,
            http_status=int(HTTPStatus.NOT_FOUND),
            severity=ErrorSeverity.WARNING,
            retryable=False,
            safe_to_expose=True,
        ),
        ErrorDefinition(
            error_code="validation_failed",
            message_key="error.request.validation_failed",
            default_message="Request validation failed.",
            domain=ErrorDomain.API,
            category=ErrorCategory.VALIDATION,
            http_status=int(HTTPStatus.BAD_REQUEST),
            severity=ErrorSeverity.WARNING,
            retryable=False,
            safe_to_expose=True,
        ),
        ErrorDefinition(
            error_code="duplicate_request",
            message_key="error.request.duplicate",
            default_message="The request conflicts with an existing resource.",
            domain=ErrorDomain.API,
            category=ErrorCategory.CONFLICT,
            http_status=int(HTTPStatus.CONFLICT),
            severity=ErrorSeverity.WARNING,
            retryable=False,
            safe_to_expose=True,
        ),
        ErrorDefinition(
            error_code="integration_unreachable",
            message_key="error.integration.unreachable",
            default_message="Integration '{integration}' is unavailable.",
            domain=ErrorDomain.INTEGRATION,
            category=ErrorCategory.UNAVAILABLE,
            http_status=int(HTTPStatus.SERVICE_UNAVAILABLE),
            severity=ErrorSeverity.WARNING,
            retryable=True,
            safe_to_expose=True,
        ),
    )
)

__all__ = ["PLATFORM_ERROR_REGISTRY"]
