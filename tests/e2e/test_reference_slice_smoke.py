from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[2]


def test_reference_slice_is_discoverable_from_runtime_and_docs(client: TestClient) -> None:
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    getting_started_text = (ROOT / "docs" / "getting-started.md").read_text(encoding="utf-8")

    response = client.get("/")
    payload = response.json()

    assert response.status_code == 200
    assert payload["service"] == "Fullstack Template API"
    assert payload["docs"] == "/docs"
    assert payload["health"] == "/api/v1/system/health"
    assert payload["readiness"] == "/api/v1/system/readyz"
    assert payload["liveness"] == "/api/v1/system/livez"

    assert "Fullstack Template" in readme_text
    assert "template baseline, not a finished product" in readme_text
    assert "Health endpoint: `http://localhost:8000/api/v1/system/health`" in readme_text
    assert "The current canonical reference slice is `system health`." in readme_text

    assert "health: `http://localhost:8000/api/v1/system/health`" in getting_started_text
    assert "The frontend works without an extra env file for local development." in getting_started_text


def test_frontend_homepage_and_feature_copy_match_the_reference_slice(client: TestClient) -> None:
    homepage_text = (
        ROOT / "src" / "frontend" / "pages" / "home" / "ui" / "HomePage.vue"
    ).read_text(encoding="utf-8")
    feature_text = (
        ROOT / "src" / "frontend" / "features" / "system-health" / "ui" / "SystemHealthPanel.vue"
    ).read_text(encoding="utf-8")
    router_text = (ROOT / "src" / "frontend" / "app" / "router" / "index.ts").read_text(encoding="utf-8")

    health_response = client.get("/api/v1/system/health")
    health_payload = health_response.json()

    assert health_response.status_code == 200
    assert health_payload["status"] == "ok"
    assert len(health_payload["checks"]) == 2

    assert 'title="This is the template baseline"' in homepage_text
    assert "intentionally not a product dashboard" in homepage_text
    assert 'title="Reference system health slice"' in feature_text
    assert "canonical /api/v1/system/health contract across backend, frontend and tests" in feature_text
    assert 'title: "Fullstack template frontend"' in router_text
