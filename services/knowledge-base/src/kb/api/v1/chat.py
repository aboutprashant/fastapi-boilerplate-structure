from fastapi import APIRouter

from kb.core.auth import ScopeDep
from kb.core.dependencies import SessionDep
from kb.domain.schemas import (
    ChatMessageCreate,
    ChatMessageRead,
    ChatSessionCreate,
    ChatSessionRead,
    FeedbackCreate,
    FeedbackResponse,
    SearchRequest,
)
from kb.generation.answer_generator import build_answer_generator
from kb.persistence.repositories.chat import ChatRepository
from kb.persistence.repositories.search import SearchRepository
from kb.retrieval.citations import build_citation
from kb.retrieval.context_assembly import assemble_context

router = APIRouter(tags=["chat"])


@router.post("/chat/sessions", response_model=ChatSessionRead)
async def create_session(
    payload: ChatSessionCreate,
    session: SessionDep,
    scope: ScopeDep,
) -> ChatSessionRead:
    chat = await ChatRepository(session).create_session(payload.project_id, payload.title, scope)
    await session.commit()
    return ChatSessionRead(
        id=chat.id,
        project_id=chat.project_id,
        title=chat.title,
        created_at=chat.created_at,
        updated_at=chat.updated_at,
    )


@router.get("/chat/sessions", response_model=list[ChatSessionRead])
async def list_sessions(session: SessionDep, scope: ScopeDep) -> list[ChatSessionRead]:
    sessions = await ChatRepository(session).list_sessions(scope)
    return [
        ChatSessionRead(
            id=item.id,
            project_id=item.project_id,
            title=item.title,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
        for item in sessions
    ]


@router.post("/chat/sessions/{session_id}/messages", response_model=ChatMessageRead)
async def add_message(
    session_id: str,
    payload: ChatMessageCreate,
    session: SessionDep,
    scope: ScopeDep,
) -> ChatMessageRead:
    chat_repository = ChatRepository(session)
    chat_session = await chat_repository.get_session(session_id, scope)
    await chat_repository.add_message(session_id, "user", payload.content, [])

    request = SearchRequest(
        query=payload.content,
        project_ids=payload.project_ids or [chat_session.project_id],
        top_k=5,
    )
    embedding = await session.info["embedding_provider"].embed(request.query)
    rows = await SearchRepository(session).search_chunks(
        query_embedding=embedding,
        scope=scope,
        requested_project_ids=request.project_ids,
        top_k=request.top_k,
        doc_type=request.doc_type,
    )
    contexts = [assemble_context(chunk, document) for chunk, document, _ in rows]
    citations = [build_citation(chunk, document) for chunk, document, _ in rows]
    answer = await build_answer_generator(True).generate(payload.content, contexts, citations)
    message = await chat_repository.add_message(
        session_id,
        "assistant",
        answer,
        [citation.model_dump(mode="json") for citation in citations],
    )
    await session.commit()
    return ChatMessageRead(
        id=message.id,
        role=message.role,
        content=message.content,
        citations=citations,
    )


@router.post("/messages/{message_id}/feedback", response_model=FeedbackResponse)
async def add_feedback(
    message_id: str,
    payload: FeedbackCreate,
    session: SessionDep,
    scope: ScopeDep,
) -> FeedbackResponse:
    feedback = await ChatRepository(session).add_feedback(message_id, payload, scope)
    await session.commit()
    return FeedbackResponse(id=feedback.id, message_id=feedback.message_id, rating=feedback.rating)
