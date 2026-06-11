from contracts import ScopeObject
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from kb.core.errors import NotFoundError
from kb.domain.schemas import DocumentCreate
from kb.persistence.models import Chunk, Document


class DocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_ingesting(self, payload: DocumentCreate, scope: ScopeObject) -> Document:
        metadata = payload.metadata
        if metadata.supersedes_document_id:
            await self.session.execute(
                update(Document)
                .where(
                    Document.id == metadata.supersedes_document_id,
                    Document.org_id == scope.organization_uuid,
                )
                .values(status="superseded")
            )

        document = Document(
            org_id=scope.organization_uuid,
            project_id=payload.project_id,
            source_context=metadata.source_context,
            name=metadata.name,
            doc_type=metadata.doc_type,
            version_date=metadata.version_date,
            supersedes_document_id=metadata.supersedes_document_id,
            notes=metadata.notes,
            storage_ref=payload.storage_ref,
            status="ingesting",
            created_by=scope.user_uuid,
        )
        self.session.add(document)
        await self.session.flush()
        return document

    async def get_for_scope(self, document_id: str, scope: ScopeObject) -> Document:
        statement = select(Document).where(
            Document.id == document_id,
            Document.org_id == scope.organization_uuid,
            Document.project_id.in_(self._allowed_projects(scope, [])),
        )
        document = await self.session.scalar(statement)
        if document is None:
            raise NotFoundError("Document not found")
        return document

    async def delete_for_scope(self, document_id: str, scope: ScopeObject) -> None:
        await self.get_for_scope(document_id, scope)
        await self.session.execute(delete(Document).where(Document.id == document_id))

    async def override_classification(self, document_id: str, scope: ScopeObject) -> Document:
        document = await self.get_for_scope(document_id, scope)
        document.classification_overridden = True
        document.status = "active"
        await self.session.flush()
        return document

    async def set_classification(
        self,
        document_id: str,
        verdict: str,
        status: str,
    ) -> None:
        await self.session.execute(
            update(Document)
            .where(Document.id == document_id)
            .values(classification_verdict=verdict, status=status)
        )

    async def add_chunks(self, chunks: list[Chunk]) -> None:
        self.session.add_all(chunks)

    def _allowed_projects(self, scope: ScopeObject, requested_project_ids: list[str]) -> list[str]:
        if scope.role == "project_user":
            return scope.project_uuids
        return requested_project_ids or scope.project_uuids
