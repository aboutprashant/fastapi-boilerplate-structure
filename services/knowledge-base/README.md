# knowledge-base

System of record for documents, positional chunks, search, citations, and chat history.

## Run

```bash
uv sync
cp .env.example .env
uv run uvicorn kb.main:app --reload
```

## Endpoints

- `GET /health`
- `GET /ready`
- `POST /api/v1/documents`
- `GET /api/v1/documents/{id}`
- `POST /api/v1/documents/{id}/override`
- `DELETE /api/v1/documents/{id}`
- `POST /api/v1/search`
- `POST /api/v1/chat/sessions`
- `GET /api/v1/chat/sessions`
- `POST /api/v1/chat/sessions/{id}/messages`
- `POST /api/v1/messages/{id}/feedback`
