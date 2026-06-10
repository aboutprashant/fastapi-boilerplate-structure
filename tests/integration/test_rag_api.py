from fastapi.testclient import TestClient


def test_ingest_and_query_documents(client: TestClient) -> None:
    ingest_response = client.post(
        "/api/v1/rag/documents",
        json={
            "documents": [
                {
                    "content": "FastAPI is a modern Python framework for building APIs.",
                    "metadata": {"source": "test-doc"},
                }
            ]
        },
    )

    assert ingest_response.status_code == 201
    assert ingest_response.json()["chunk_count"] == 1

    query_response = client.post(
        "/api/v1/rag/query",
        json={"question": "What is FastAPI?", "top_k": 1},
    )

    payload = query_response.json()
    assert query_response.status_code == 200
    assert "FastAPI" in payload["answer"]
    assert payload["sources"][0]["metadata"]["source"] == "test-doc"
