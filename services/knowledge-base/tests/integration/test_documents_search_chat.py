from fastapi.testclient import TestClient
from tests.conftest import make_token


def _document_payload(project_id: str, content: str, doc_type: str = "donor_agreement") -> dict:
    return {
        "project_id": project_id,
        "metadata": {
            "name": f"{project_id} document",
            "doc_type": doc_type,
            "version_date": "2026-01-01",
            "source_context": "details_files",
        },
        "content": content,
    }


def test_upload_get_override_and_search(client: TestClient, auth_header: dict[str, str]) -> None:
    response = client.post(
        "/api/v1/documents",
        json=_document_payload("project-a", "progress report content", "donor_agreement"),
        headers=auth_header,
    )
    assert response.status_code == 202
    document_id = response.json()["document_id"]

    document = client.get(f"/api/v1/documents/{document_id}", headers=auth_header)
    assert document.status_code == 200
    assert document.json()["classification_verdict"] == "orange"

    override = client.post(f"/api/v1/documents/{document_id}/override", headers=auth_header)
    assert override.status_code == 200
    assert override.json()["status"] == "active"

    search = client.post(
        "/api/v1/search",
        json={"query": "progress report", "project_ids": ["project-a"]},
        headers=auth_header,
    )
    assert search.status_code == 200
    assert search.json()["results"][0]["citation"]["link"].endswith("#page=1")


def test_project_user_cannot_read_another_projects_chunks(
    client: TestClient,
    auth_header: dict[str, str],
) -> None:
    for project_id, content in [
        ("project-a", "donor commitment alpha"),
        ("project-b", "donor commitment beta"),
    ]:
        response = client.post(
            "/api/v1/documents",
            json=_document_payload(project_id, content),
            headers=auth_header,
        )
        assert response.status_code == 202

    user_header = {"Authorization": f"Bearer {make_token(['project-a'], 'project_user')}"}
    search = client.post(
        "/api/v1/search",
        json={"query": "donor commitment", "project_ids": ["project-b"], "top_k": 10},
        headers=user_header,
    )

    assert search.status_code == 200
    results = search.json()["results"]
    assert results
    assert all("project-a document" in result["content"] for result in results)


def test_delete_removes_chunks_from_search(client: TestClient, auth_header: dict[str, str]) -> None:
    response = client.post(
        "/api/v1/documents",
        json=_document_payload("project-a", "unique deletion marker"),
        headers=auth_header,
    )
    document_id = response.json()["document_id"]

    found = client.post(
        "/api/v1/search",
        json={"query": "unique deletion marker", "project_ids": ["project-a"]},
        headers=auth_header,
    )
    assert found.json()["results"]

    delete = client.delete(f"/api/v1/documents/{document_id}", headers=auth_header)
    assert delete.status_code == 204

    missing = client.post(
        "/api/v1/search",
        json={"query": "unique deletion marker", "project_ids": ["project-a"]},
        headers=auth_header,
    )
    assert missing.json()["results"] == []


def test_chat_routes(client: TestClient, auth_header: dict[str, str]) -> None:
    client.post(
        "/api/v1/documents",
        json=_document_payload("project-a", "donor agreement chat context"),
        headers=auth_header,
    )
    session = client.post(
        "/api/v1/chat/sessions",
        json={"project_id": "project-a", "title": "Donor review"},
        headers=auth_header,
    )
    assert session.status_code == 200
    session_id = session.json()["id"]

    sessions = client.get("/api/v1/chat/sessions", headers=auth_header)
    assert sessions.status_code == 200
    assert sessions.json()[0]["title"] == "Donor review"

    message = client.post(
        f"/api/v1/chat/sessions/{session_id}/messages",
        json={"content": "What does the donor agreement say?"},
        headers=auth_header,
    )
    assert message.status_code == 200
    message_id = message.json()["id"]

    feedback = client.post(
        f"/api/v1/messages/{message_id}/feedback",
        json={"rating": "up", "comment": "useful"},
        headers=auth_header,
    )
    assert feedback.status_code == 200
    assert feedback.json()["rating"] == "up"
