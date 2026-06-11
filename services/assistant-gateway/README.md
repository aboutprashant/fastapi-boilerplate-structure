# Assistant Gateway

Conversational entry point for the AI platform. It classifies user intent, routes to knowledge-base or analytics workflows, and synthesizes a final answer.

## Run Standalone

```bash
uv sync
cp .env.example .env
uv run uvicorn gateway.main:app --reload
```

## Endpoints

- `GET /health`
- `GET /ready`
- `GET /metrics`
- `POST /api/v1/chat`

The default graph uses deterministic mock LLM and service clients so tests run offline.
