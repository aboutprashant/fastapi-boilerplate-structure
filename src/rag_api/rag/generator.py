from typing import Protocol

from rag_api.rag.vector_store import SearchResult


class AnswerGenerator(Protocol):
    def generate(self, question: str, context: list[SearchResult]) -> str:
        raise NotImplementedError


class ExtractiveAnswerGenerator:
    """Local answer generator that returns a concise answer from retrieved snippets."""

    def generate(self, question: str, context: list[SearchResult]) -> str:
        if not context:
            return "I could not find relevant context for that question."

        snippets = [result.chunk.content for result in context if result.score > 0]
        if not snippets:
            return "I could not find relevant context for that question."

        joined = " ".join(snippets)
        return f"Based on the retrieved context: {joined[:700]}"
