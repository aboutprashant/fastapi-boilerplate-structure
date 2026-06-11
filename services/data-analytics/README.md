# data-analytics

Guarded NL2SQL analytics service with deterministic mock generation.

## Run

```bash
uv sync
cp .env.example .env
uv run uvicorn analytics.main:app --reload
```

## Endpoints

- `GET /health`
- `GET /ready`
- `POST /api/v1/nl2sql/query`
- `GET /api/v1/schema/{project_id}`
