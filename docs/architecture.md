# Architecture

This boilerplate keeps the RAG workflow small and replaceable.

1. API routes receive ingestion or query requests.
2. `RagService` coordinates chunking, embedding, storage, retrieval, and answer generation.
3. `EmbeddingProvider`, `VectorStore`, and `AnswerGenerator` are interfaces that can be replaced with production providers.
4. Logging, health checks, readiness checks, and Prometheus metrics are configured at the app boundary.

The default implementation is useful for local development, CI, and proving the API contract. Production deployments should back the vector store with a persistent database and use provider-backed embeddings and generation.
