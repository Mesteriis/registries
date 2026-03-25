import pytest
from core.bootstrap import create_app
from core.errors import (
    DuplicateErrorCodeError,
    ErrorCategory,
    ErrorDefinition,
    ErrorDomain,
    ErrorRegistry,
    ErrorSeverity,
    ResourceNotFoundError,
)
from fastapi.testclient import TestClient


def test_error_registry_rejects_duplicate_error_codes() -> None:
    registry = ErrorRegistry(
        definitions=(
            ErrorDefinition(
                error_code="test_error",
                message_key="error.test.one",
                default_message="Test error.",
                domain=ErrorDomain.CORE,
                category=ErrorCategory.INTERNAL,
                http_status=500,
                severity=ErrorSeverity.ERROR,
            ),
        )
    )

    with pytest.raises(DuplicateErrorCodeError):
        registry.register(
            ErrorDefinition(
                error_code="test_error",
                message_key="error.test.two",
                default_message="Another test error.",
                domain=ErrorDomain.CORE,
                category=ErrorCategory.INTERNAL,
                http_status=500,
                severity=ErrorSeverity.ERROR,
            )
        )


def test_platform_error_handler_returns_structured_payload() -> None:
    app = create_app()

    @app.get("/test-errors/not-found")
    async def read_missing() -> None:
        raise ResourceNotFoundError(resource="system probe")

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/test-errors/not-found")

    assert response.status_code == 404
    assert response.json() == {
        "code": "resource_not_found",
        "message": "Requested system probe was not found.",
        "message_key": "error.resource.not_found",
        "domain": "api",
        "category": "not_found",
        "http_status": 404,
        "severity": "warning",
        "safe_to_expose": True,
        "details": [],
        "retryable": False,
        "request_id": response.headers["x-request-id"],
        "correlation_id": response.headers["x-correlation-id"],
    }


def test_request_validation_handler_returns_structured_payload() -> None:
    app = create_app()

    @app.get("/test-errors/validation")
    async def read_validation(limit: int) -> dict[str, int]:
        return {"limit": limit}

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/test-errors/validation", params={"limit": "bad"})

    assert response.status_code == 400
    payload = response.json()

    assert payload["code"] == "validation_failed"
    assert payload["message"] == "Request validation failed."
    assert payload["message_key"] == "error.request.validation_failed"
    assert payload["request_id"] == response.headers["x-request-id"]
    assert payload["correlation_id"] == response.headers["x-correlation-id"]
    assert payload["details"][0]["field"] == "query.limit"


def test_unhandled_error_handler_returns_internal_payload() -> None:
    app = create_app()

    @app.get("/test-errors/unhandled")
    async def read_unhandled() -> None:
        raise RuntimeError("boom")

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/test-errors/unhandled")

    assert response.status_code == 500
    assert response.json() == {
        "code": "internal_error",
        "message": "Internal server error.",
        "message_key": "error.system.internal",
        "domain": "core",
        "category": "internal",
        "http_status": 500,
        "severity": "error",
        "safe_to_expose": False,
        "details": [],
        "retryable": False,
        "request_id": response.headers["x-request-id"],
        "correlation_id": response.headers["x-correlation-id"],
    }
