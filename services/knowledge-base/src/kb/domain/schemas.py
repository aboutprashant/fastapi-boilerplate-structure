from datetime import datetime
from typing import Literal

from contracts import Citation, DocumentMetadata
from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    project_id: str
    metadata: DocumentMetadata
    content: str = Field(..., min_length=1)
    storage_ref: str | None = None


class DocumentCreateResponse(BaseModel):
    document_id: str
    status: Literal["ingesting"]


class DocumentRead(BaseModel):
    id: str
    project_id: str
    name: str
    doc_type: str
    status: str
    classification_verdict: str | None
    classification_overridden: bool


class OverrideResponse(BaseModel):
    document_id: str
    status: str
    classification_overridden: bool


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    project_ids: list[str] = []
    doc_type: str | None = None
    top_k: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    document_id: str
    content: str
    score: float
    citation: Citation


class SearchResponse(BaseModel):
    results: list[SearchResult]


class ChatSessionCreate(BaseModel):
    project_id: str
    title: str = "New chat"


class ChatSessionRead(BaseModel):
    id: str
    project_id: str
    title: str
    created_at: datetime
    updated_at: datetime


class ChatMessageCreate(BaseModel):
    content: str = Field(..., min_length=1)
    project_ids: list[str] = []


class ChatMessageRead(BaseModel):
    id: str
    role: str
    content: str
    citations: list[Citation]


class FeedbackCreate(BaseModel):
    rating: Literal["up", "down"]
    comment: str | None = None


class FeedbackResponse(BaseModel):
    id: str
    message_id: str
    rating: str
