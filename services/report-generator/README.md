# report-generator

Scaffold for report job orchestration. Legacy report code migrates into this service.

## Run

```bash
uv sync
cp .env.example .env
uv run uvicorn reports.main:app --reload
```

## Endpoints

- `GET /health`
- `GET /ready`
- `POST /api/v1/reports/generate`
- `GET /api/v1/reports/{id}`
- `GET /api/v1/reports/{id}/download`
