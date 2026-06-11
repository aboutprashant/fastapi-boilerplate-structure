from fastapi.testclient import TestClient


def test_health_ready_nl2sql_and_schema(client: TestClient, auth_header: dict[str, str]) -> None:
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/ready").json()["checks"]["database"] is True

    query = client.post(
        "/api/v1/nl2sql/query",
        json={"question": "How many activities are complete?"},
        headers=auth_header,
    )
    assert query.status_code == 200
    assert query.json()["columns"] == ["metric_name", "value"]

    schema = client.get("/api/v1/schema/project-a", headers=auth_header)
    assert schema.status_code == 200
    assert "project_metrics" in schema.json()["tables"]
