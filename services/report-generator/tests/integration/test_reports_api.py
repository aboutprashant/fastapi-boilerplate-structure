from fastapi.testclient import TestClient


def test_health_ready_and_report_routes(client: TestClient, auth_header: dict[str, str]) -> None:
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/ready").json()["checks"]["database"] is True

    created = client.post(
        "/api/v1/reports/generate",
        json={"project_id": "project-a", "prompt": "Generate quarterly report"},
        headers=auth_header,
    )
    assert created.status_code == 200
    report_id = created.json()["report_id"]

    read = client.get(f"/api/v1/reports/{report_id}", headers=auth_header)
    assert read.status_code == 200
    assert read.json()["project_id"] == "project-a"

    download = client.get(f"/api/v1/reports/{report_id}/download", headers=auth_header)
    assert download.status_code == 200
    assert download.json()["download_url"].endswith(".pdf")
