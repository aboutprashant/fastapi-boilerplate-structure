# ai-platform

Production-grade Python monorepo for standalone AI platform services.

Each service under `services/` is a self-contained FastAPI application with its own
`pyproject.toml`, `uv.lock`, `Dockerfile`, tests, and `.env.example`. Services do not
import code from each other. The only shared Python package is `shared/contracts`, which
contains Pydantic schemas only.

## Services

- `services/knowledge-base`: document system of record, retrieval, citations, and chat history.
- `services/report-generator`: report job orchestration scaffold.
- `services/data-analytics`: guarded NL2SQL scaffold.
- `services/assistant-gateway`: conversational gateway with LangGraph routing.

## Local Commands

```bash
make lint
make test
make dev SERVICE=knowledge-base
```

Run a service standalone:

```bash
cd services/knowledge-base
uv sync
uv run uvicorn kb.main:app --reload
```

Run the local stack:

```bash
docker compose -f infra/docker-compose.yml up --build
```
