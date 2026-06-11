from datetime import date
from typing import Literal

from pydantic import BaseModel


class ScopeObject(BaseModel):
    organization_uuid: str
    user_uuid: str
    user_email: str
    role: str
    project_uuids: list[str]


class DocumentMetadata(BaseModel):
    name: str
    doc_type: str
    version_date: date
    supersedes_document_id: str | None = None
    notes: str | None = None
    source_context: Literal["details_files", "indicator_evidence", "activity_report"]


class Citation(BaseModel):
    document_id: str
    title: str
    doc_type: str
    version_date: date
    page: int
    line_start: int | None = None
    line_end: int | None = None
    quote: str
    link: str


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    citations: list[Citation] = []
