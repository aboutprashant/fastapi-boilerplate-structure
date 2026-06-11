from fastapi.testclient import TestClient


def test_health_and_ready(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok"}

    ready = client.get("/ready")
    assert ready.status_code == 200
    assert ready.json()["checks"]["database"] is True
