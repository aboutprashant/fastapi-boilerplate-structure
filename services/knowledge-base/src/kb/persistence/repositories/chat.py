from contracts import ScopeObject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from kb.core.errors import NotFoundError
from kb.domain.schemas import FeedbackCreate
from kb.persistence.models import ChatSession, Message, MessageFeedback


class ChatRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_session(self, project_id: str, title: str, scope: ScopeObject) -> ChatSession:
        session = ChatSession(
            org_id=scope.organization_uuid,
            project_id=project_id,
            user_id=scope.user_uuid,
            title=title,
        )
        self.session.add(session)
        await self.session.flush()
        return session

    async def list_sessions(self, scope: ScopeObject) -> list[ChatSession]:
        statement = (
            select(ChatSession)
            .where(
                ChatSession.org_id == scope.organization_uuid,
                ChatSession.project_id.in_(self._allowed_projects(scope)),
                ChatSession.user_id == scope.user_uuid,
            )
            .order_by(ChatSession.updated_at.desc())
        )
        return list((await self.session.scalars(statement)).all())

    async def get_session(self, session_id: str, scope: ScopeObject) -> ChatSession:
        statement = select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.org_id == scope.organization_uuid,
            ChatSession.project_id.in_(self._allowed_projects(scope)),
        )
        session = await self.session.scalar(statement)
        if session is None:
            raise NotFoundError("Chat session not found")
        return session

    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        citations: list[dict],
    ) -> Message:
        message = Message(
            session_id=session_id,
            role=role,
            content=content,
            citations=citations,
        )
        self.session.add(message)
        await self.session.flush()
        return message

    async def add_feedback(
        self,
        message_id: str,
        payload: FeedbackCreate,
        scope: ScopeObject,
    ) -> MessageFeedback:
        feedback = MessageFeedback(
            message_id=message_id,
            user_id=scope.user_uuid,
            rating=payload.rating,
            comment=payload.comment,
        )
        self.session.add(feedback)
        await self.session.flush()
        return feedback

    def _allowed_projects(self, scope: ScopeObject) -> list[str]:
        return scope.project_uuids
