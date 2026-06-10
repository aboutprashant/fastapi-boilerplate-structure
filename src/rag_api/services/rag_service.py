from rag_api.core.config import Settings
from rag_api.models.rag import DocumentInput, IngestResponse, QueryResponse, SourceDocument
from rag_api.rag.chunking import chunk_text
from rag_api.rag.embeddings import EmbeddingProvider, HashEmbeddingProvider
from rag_api.rag.generator import AnswerGenerator, ExtractiveAnswerGenerator
from rag_api.rag.retriever import Retriever
from rag_api.rag.vector_store import DocumentChunk, InMemoryVectorStore, VectorStore


class RagService:
    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
        answer_generator: AnswerGenerator,
        default_top_k: int,
        max_upload_chars: int,
    ) -> None:
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store
        self.answer_generator = answer_generator
        self.retriever = Retriever(embedding_provider, vector_store)
        self.default_top_k = default_top_k
        self.max_upload_chars = max_upload_chars

    def ingest(self, documents: list[DocumentInput]) -> IngestResponse:
        chunks: list[DocumentChunk] = []

        for index, document in enumerate(documents):
            content = document.content[: self.max_upload_chars]
            for chunk_index, chunk in enumerate(chunk_text(content)):
                metadata = {
                    **document.metadata,
                    "document_index": index,
                    "chunk_index": chunk_index,
                }
                chunks.append(
                    DocumentChunk(
                        content=chunk,
                        embedding=self.embedding_provider.embed(chunk),
                        metadata=metadata,
                    )
                )

        self.vector_store.add(chunks)
        return IngestResponse(document_count=len(documents), chunk_count=len(chunks))

    def query(self, question: str, top_k: int | None = None) -> QueryResponse:
        results = self.retriever.retrieve(question, top_k=top_k or self.default_top_k)
        answer = self.answer_generator.generate(question, results)
        sources = [
            SourceDocument(
                content=result.chunk.content,
                score=round(result.score, 4),
                metadata=result.chunk.metadata,
            )
            for result in results
        ]
        return QueryResponse(answer=answer, sources=sources)


def build_rag_service(settings: Settings) -> RagService:
    return RagService(
        embedding_provider=HashEmbeddingProvider(dimensions=settings.embedding_dimension),
        vector_store=InMemoryVectorStore(),
        answer_generator=ExtractiveAnswerGenerator(),
        default_top_k=settings.rag_top_k,
        max_upload_chars=settings.max_upload_chars,
    )
