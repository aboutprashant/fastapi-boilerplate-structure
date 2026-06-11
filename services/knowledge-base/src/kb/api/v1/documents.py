from fastapi import APIRouter, status

from kb.core.auth import ScopeDep
from kb.core.dependencies import SessionDep
from kb.domain.schemas import (
    DocumentCreate,
    DocumentCreateResponse,
    DocumentRead,
    OverrideResponse,
)
from kb.persistence.repositories.documents import DocumentRepository
from kb.workers.tasks import LocalIngestionQueue

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentCreateResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    payload: DocumentCreate,
    session: SessionDep,
    scope: ScopeDep,
) -> DocumentCreateResponse:
    repository = DocumentRepository(session)
    document = await repository.create_ingesting(payload, scope)
    await LocalIngestionQueue().enqueue(
        session=session,
        document=document,
        content=payload.content,
        scope=scope,
        embedding_provider=session.info["embedding_provider"],
    )
    await session.commit()
    return DocumentCreateResponse(document_id=document.id, status="ingesting")


@router.get("/{document_id}", response_model=DocumentRead)
async def get_document(
    document_id: str,
    session: SessionDep,
    scope: ScopeDep,
) -> DocumentRead:
    document = await DocumentRepository(session).get_for_scope(document_id, scope)
    return DocumentRead(
        id=document.id,
        project_id=document.project_id,
        name=document.name,
        doc_type=document.doc_type,
        status=document.status,
        classification_verdict=document.classification_verdict,
        classification_overridden=document.classification_overridden,
    )


@router.post("/{document_id}/override", response_model=OverrideResponse)
async def override_document(
    document_id: str,
    session: SessionDep,
    scope: ScopeDep,
) -> OverrideResponse:
    document = await DocumentRepository(session).override_classification(document_id, scope)
    await session.commit()
    return OverrideResponse(
        document_id=document.id,
        status=document.status,
        classification_overridden=document.classification_overridden,
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    session: SessionDep,
    scope: ScopeDep,
) -> None:
    await DocumentRepository(session).delete_for_scope(document_id, scope)
    await session.commit()
