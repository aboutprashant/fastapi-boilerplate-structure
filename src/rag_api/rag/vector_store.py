from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import uuid4


@dataclass(slots=True)
class DocumentChunk:
    content: str
    embedding: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass(slots=True)
class SearchResult:
    chunk: DocumentChunk
    score: float


class VectorStore(Protocol):
    def add(self, chunks: list[DocumentChunk]) -> None:
        raise NotImplementedError

    def similarity_search(self, embedding: list[float], top_k: int) -> list[SearchResult]:
        raise NotImplementedError


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._chunks: list[DocumentChunk] = []

    def add(self, chunks: list[DocumentChunk]) -> None:
        self._chunks.extend(chunks)

    def similarity_search(self, embedding: list[float], top_k: int) -> list[SearchResult]:
        scored = [
            SearchResult(chunk=chunk, score=_cosine_similarity(embedding, chunk.embedding))
            for chunk in self._chunks
        ]
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    return sum(a * b for a, b in zip(left, right, strict=True))
