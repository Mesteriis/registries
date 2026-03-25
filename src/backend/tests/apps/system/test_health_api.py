from fastapi.testclient import TestClient


def test_root_returns_service_metadata(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "service": "Registries API",
        "docs": "/docs",
        "health": "/api/v1/system/health",
        "liveness": "/api/v1/system/livez",
        "readiness": "/api/v1/system/readyz",
    }


def test_liveness_endpoint_returns_ok_status(client: TestClient) -> None:
    response = client.get("/api/v1/system/livez")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Registries API"}
