from typing import Any

from pydantic import BaseModel, Field


class DocumentInput(BaseModel):
    content: str = Field(..., min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class IngestRequest(BaseModel):
    documents: list[DocumentInput] = Field(..., min_length=1)


class IngestResponse(BaseModel):
    document_count: int
    chunk_count: int


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int | None = Field(default=None, ge=1, le=20)


class SourceDocument(BaseModel):
    content: str
    score: float
    metadata: dict[str, Any]


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]
