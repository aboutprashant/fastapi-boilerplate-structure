import math

from contracts import ScopeObject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from kb.persistence.models import Chunk, Document


class SearchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def search_chunks(
        self,
        query_embedding: list[float],
        scope: ScopeObject,
        requested_project_ids: list[str],
        top_k: int,
        doc_type: str | None = None,
    ) -> list[tuple[Chunk, Document, float]]:
        allowed_projects = self._allowed_projects(scope, requested_project_ids)
        statement = (
            select(Chunk, Document)
            .join(Document, Document.id == Chunk.document_id)
            .where(
                Chunk.org_id == scope.organization_uuid,
                Chunk.project_id.in_(allowed_projects),
                Document.status == "active",
            )
        )
        if doc_type:
            statement = statement.where(Document.doc_type == doc_type)

        rows = (await self.session.execute(statement)).all()
        scored = [
            (chunk, document, _cosine_similarity(query_embedding, chunk.embedding))
            for chunk, document in rows
        ]
        scored.sort(key=lambda item: item[2], reverse=True)
        return scored[:top_k]

    def _allowed_projects(self, scope: ScopeObject, requested_project_ids: list[str]) -> list[str]:
        if scope.role == "project_user":
            return scope.project_uuids
        return requested_project_ids or scope.project_uuids


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    numerator = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)
