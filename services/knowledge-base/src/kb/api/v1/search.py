from fastapi import APIRouter

from kb.core.auth import ScopeDep
from kb.core.dependencies import SessionDep
from kb.domain.schemas import SearchRequest, SearchResponse, SearchResult
from kb.persistence.repositories.search import SearchRepository
from kb.retrieval.citations import build_citation
from kb.retrieval.context_assembly import assemble_context

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=SearchResponse)
async def search(
    payload: SearchRequest,
    session: SessionDep,
    scope: ScopeDep,
) -> SearchResponse:
    embedding = await session.info["embedding_provider"].embed(payload.query)
    rows = await SearchRepository(session).search_chunks(
        query_embedding=embedding,
        scope=scope,
        requested_project_ids=payload.project_ids,
        top_k=payload.top_k,
        doc_type=payload.doc_type,
    )
    return SearchResponse(
        results=[
            SearchResult(
                document_id=document.id,
                content=assemble_context(chunk, document),
                score=round(score, 4),
                citation=build_citation(chunk, document),
            )
            for chunk, document, score in rows
        ]
    )
