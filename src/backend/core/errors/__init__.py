from core.errors.catalog import PLATFORM_ERROR_REGISTRY
from core.errors.exceptions import (
    DuplicateRequestError,
    IntegrationUnreachableError,
    InternalPlatformError,
    PlatformError,
    RegistryBackedPlatformError,
    ResourceNotFoundError,
    ValidationFailedError,
)
from core.errors.registry import (
    DuplicateErrorCodeError,
    DuplicateMessageKeyError,
    ErrorDefinition,
    ErrorRegistry,
    ErrorRegistryError,
    UnknownErrorCodeError,
    UnknownMessageKeyError,
)
from core.errors.taxonomy import ErrorCategory, ErrorDomain, ErrorSeverity

__all__ = [
    "PLATFORM_ERROR_REGISTRY",
    "DuplicateErrorCodeError",
    "DuplicateMessageKeyError",
    "DuplicateRequestError",
    "ErrorCategory",
    "ErrorDefinition",
    "ErrorDomain",
    "ErrorRegistry",
    "ErrorRegistryError",
    "ErrorSeverity",
    "IntegrationUnreachableError",
    "InternalPlatformError",
    "PlatformError",
    "RegistryBackedPlatformError",
    "ResourceNotFoundError",
    "UnknownErrorCodeError",
    "UnknownMessageKeyError",
    "ValidationFailedError",
]
