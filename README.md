# FastAPI RAG Pipeline

A straightforward FastAPI starter for retrieval augmented generation (RAG) services. It runs out of the box with an in-memory vector store and deterministic local embeddings, then leaves clean seams for production providers such as OpenAI embeddings, pgvector, Pinecone, Weaviate, or a managed LLM gateway.

## What Is Included

- FastAPI app factory with versioned API routes.
- Health and readiness endpoints.
- RAG ingestion and query endpoints.
- Deterministic local embedding provider for tests and local demos.
- In-memory vector store behind a replaceable interface.
- Structured JSON logging with request timing.
- Prometheus metrics at `/metrics`.
- Pytest test suite with API and RAG flow coverage.
- Dockerfile, docker-compose, Prometheus config, and GitHub Actions CI.
- `uv` based dependency and command workflow.

## Project Layout

```text
.
├── src/rag_api
│   ├── api/v1          # Versioned route modules
│   ├── core            # Config, logging, monitoring, dependencies
│   ├── models          # Pydantic request/response schemas
│   ├── rag             # Chunking, embeddings, retrieval, vector store
│   ├── services        # Application use-cases
│   └── main.py         # FastAPI app factory
├── tests
│   ├── integration
│   └── unit
├── monitoring
├── docker-compose.yml
├── Dockerfile
└── pyproject.toml
```

## Local Development

```bash
uv venv
uv sync
cp .env.example .env
uv run uvicorn rag_api.main:app --reload
```

The API will be available at `http://localhost:8000`.

Useful endpoints:

- `GET /health`
- `GET /ready`
- `GET /metrics`
- `POST /api/v1/rag/documents`
- `POST /api/v1/rag/query`

## Example Request

```bash
curl -X POST http://localhost:8000/api/v1/rag/documents \
  -H "Content-Type: application/json" \
  -d '{"documents":[{"content":"FastAPI is a Python framework for building APIs.","metadata":{"source":"demo"}}]}'

curl -X POST http://localhost:8000/api/v1/rag/query \
  -H "Content-Type: application/json" \
  -d '{"question":"What is FastAPI?","top_k":3}'
```

## Quality Checks

```bash
uv run ruff check .
uv run pytest
```

## Docker

```bash
docker compose up --build
```

Services:

- API: `http://localhost:8000`
- Prometheus: `http://localhost:9090`

## Production Notes

The default RAG implementation is intentionally local and deterministic. For production, replace `HashEmbeddingProvider`, `InMemoryVectorStore`, and `ExtractiveAnswerGenerator` with provider-backed implementations while keeping the `RagService` contract intact.
