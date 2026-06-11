from typing import Any, Protocol

import httpx
import jwt
from contracts import Citation, ScopeObject


class PlatformTools(Protocol):
    async def search_knowledge_base(
        self,
        query: str,
        scope: ScopeObject,
        doc_type: str | None = None,
    ) -> tuple[list[str], list[Citation]]:
        raise NotImplementedError

    async def query_analytics(self, question: str, scope: ScopeObject) -> dict[str, Any]:
        raise NotImplementedError


class HTTPPlatformTools:
    def __init__(self, knowledge_base_url: str, data_analytics_url: str, jwt_secret: str) -> None:
        self.knowledge_base_url = knowledge_base_url.rstrip("/")
        self.data_analytics_url = data_analytics_url.rstrip("/")
        self.jwt_secret = jwt_secret

    async def search_knowledge_base(
        self,
        query: str,
        scope: ScopeObject,
        doc_type: str | None = None,
    ) -> tuple[list[str], list[Citation]]:
        token = _service_token(scope, self.jwt_secret)
        payload: dict[str, Any] = {"query": query, "project_ids": scope.project_uuids, "top_k": 5}
        if doc_type:
            payload["doc_type"] = doc_type
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{self.knowledge_base_url}/api/v1/search",
                json=payload,
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
        body = response.json()
        contexts = [item["content"] for item in body["results"]]
        citations = [Citation.model_validate(item["citation"]) for item in body["results"]]
        return contexts, citations

    async def query_analytics(self, question: str, scope: ScopeObject) -> dict[str, Any]:
        token = _service_token(scope, self.jwt_secret)
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{self.data_analytics_url}/api/v1/nl2sql/query",
                json={"question": question},
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
        return response.json()


class MockPlatformTools:
    async def search_knowledge_base(
        self,
        query: str,
        scope: ScopeObject,
        doc_type: str | None = None,
    ) -> tuple[list[str], list[Citation]]:
        selected_type = doc_type or "progress_report"
        context = (
            f"[Doc: Mock {selected_type} | Type: {selected_type} | Version: 2026-01-01 | Page 1]\n"
            f"Mock context for {query} in projects {', '.join(scope.project_uuids)}."
        )
        citation = Citation(
            document_id=f"mock-{selected_type}",
            title=f"Mock {selected_type}",
            doc_type=selected_type,
            version_date="2026-01-01",
            page=1,
            line_start=1,
            line_end=3,
            quote=context,
            link=f"/documents/mock-{selected_type}/view#page=1",
        )
        return [context], [citation]

    async def query_analytics(self, question: str, scope: ScopeObject) -> dict[str, Any]:
        return {
            "sql": "select project_id, status from project_metrics limit 10",
            "rows": [{"project_id": scope.project_uuids[0], "status": "on_track"}],
            "columns": ["project_id", "status"],
            "warnings": [],
            "question": question,
        }


def _service_token(scope: ScopeObject, jwt_secret: str) -> str:
    return jwt.encode(scope.model_dump(), jwt_secret, algorithm="HS256")
