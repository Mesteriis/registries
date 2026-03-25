from enum import StrEnum


class ErrorDomain(StrEnum):
    CORE = "core"
    API = "api"
    INTEGRATION = "integration"


class ErrorCategory(StrEnum):
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    CONFLICT = "conflict"
    INTERNAL = "internal"
    NOT_FOUND = "not_found"
    POLICY = "policy"
    UNAVAILABLE = "unavailable"
    VALIDATION = "validation"


class ErrorSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


__all__ = ["ErrorCategory", "ErrorDomain", "ErrorSeverity"]
