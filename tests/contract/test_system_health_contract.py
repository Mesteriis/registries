from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[2]


def test_system_health_contract_is_aligned_across_spec_backend_and_frontend(
    client: TestClient,
    reverse: Callable[[str], str],
) -> None:
    root_response = client.get("/")
    root_payload = root_response.json()

    assert root_response.status_code == 200
    assert root_payload["health"] == reverse("read_health")
    assert root_payload["readiness"] == reverse("read_readiness")
    assert root_payload["liveness"] == reverse("read_liveness")

    health_response = client.get(root_payload["health"])
    health_payload = health_response.json()

    assert health_response.status_code == 200
    assert health_payload == {
        "status": "ok",
        "service": "Fullstack Template API",
        "checks": [
            {"name": "postgres", "status": "ok", "detail": None},
            {"name": "redis", "status": "ok", "detail": None},
        ],
    }

    spec_text = (ROOT / "specs" / "openapi" / "platform.openapi.yaml").read_text(encoding="utf-8")
    generated_api_text = (
        ROOT / "src" / "frontend" / "shared" / "api" / "generated" / "platform-api.ts"
    ).read_text(encoding="utf-8")
    frontend_shared_api_index_text = (
        ROOT / "src" / "frontend" / "shared" / "api" / "index.ts"
    ).read_text(encoding="utf-8")
    frontend_client_text = (
        ROOT / "src" / "frontend" / "entities" / "system" / "api" / "get-system-health.ts"
    ).read_text(encoding="utf-8")
    frontend_model_text = (
        ROOT / "src" / "frontend" / "entities" / "system" / "model" / "system-health.ts"
    ).read_text(encoding="utf-8")

    assert "/api/v1/system/health:" in spec_text
    assert "/api/v1/system/readyz:" in spec_text
    assert "/api/v1/system/livez:" in spec_text
    assert '$ref: "#/components/schemas/ReadinessProbe"' in spec_text
    assert "DependencyProbe" in spec_text
    assert "checks:" in spec_text

    assert 'readHealth: "/api/v1/system/health"' in generated_api_text
    assert "export interface ReadinessProbe" in generated_api_text
    assert "checks: readonly DependencyProbe[];" in generated_api_text
    assert 'export * from "@/shared/api/generated/platform-api";' in frontend_shared_api_index_text
    assert "readHealth(httpClient)" in frontend_client_text
    assert 'export type { DependencyProbe, ReadinessProbe } from "@/shared/api";' in frontend_model_text
    assert 'export type SystemHealthStatus = ReadinessProbe["status"];' in frontend_model_text


def test_error_health_contract_keeps_the_same_shape(
    app_factory: Callable[..., FastAPI],
) -> None:
    app = app_factory(health_status="error")

    with TestClient(app) as client:
        response = client.get(app.url_path_for("read_health"))

    payload = response.json()

    assert response.status_code == 503
    assert set(payload) == {"status", "service", "checks"}
    assert payload["status"] == "error"
    assert payload["service"] == "Fullstack Template API"
    assert payload["checks"] == [
        {"name": "postgres", "status": "error", "detail": "database unavailable"},
        {"name": "redis", "status": "ok", "detail": None},
    ]
