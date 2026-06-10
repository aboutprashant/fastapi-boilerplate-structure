from typing import Annotated

from fastapi import APIRouter, Depends, status

from rag_api.core.dependencies import get_rag_service
from rag_api.models.rag import IngestRequest, IngestResponse, QueryRequest, QueryResponse
from rag_api.services.rag_service import RagService

router = APIRouter()
RagServiceDep = Annotated[RagService, Depends(get_rag_service)]


@router.post("/documents", response_model=IngestResponse, status_code=status.HTTP_201_CREATED)
async def ingest_documents(
    payload: IngestRequest,
    rag_service: RagServiceDep,
) -> IngestResponse:
    return rag_service.ingest(payload.documents)


@router.post("/query", response_model=QueryResponse)
async def query_documents(
    payload: QueryRequest,
    rag_service: RagServiceDep,
) -> QueryResponse:
    return rag_service.query(payload.question, top_k=payload.top_k)
