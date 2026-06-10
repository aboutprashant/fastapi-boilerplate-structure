from rag_api.rag.embeddings import EmbeddingProvider
from rag_api.rag.vector_store import SearchResult, VectorStore


class Retriever:
    def __init__(self, embedding_provider: EmbeddingProvider, vector_store: VectorStore) -> None:
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int) -> list[SearchResult]:
        query_embedding = self.embedding_provider.embed(query)
        return self.vector_store.similarity_search(query_embedding, top_k=top_k)
