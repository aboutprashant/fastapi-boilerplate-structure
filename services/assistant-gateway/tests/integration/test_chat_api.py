from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint_returns_mock_answer(
    client: TestClient,
    auth_header: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/chat",
        json={"message": "What does the donor agreement say?"},
        headers=auth_header,
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["intent"] == "kb_lookup"
    assert payload["citations"]
