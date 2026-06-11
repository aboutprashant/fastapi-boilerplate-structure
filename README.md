# ai-platform

Production-grade Python monorepo for standalone AI platform services.

The core rule is simple: every service under `services/` is independently runnable. Each
service owns its own FastAPI app, `pyproject.toml`, `uv.lock`, `Dockerfile`, tests, and
`.env.example`. Services do not import Python code from each other; they communicate over
HTTP. The only shared package is `shared/contracts`, which contains Pydantic schemas only.

## Repository Layout

```text
.
├── services/
│   ├── knowledge-base/
│   ├── report-generator/
│   ├── data-analytics/
│   └── assistant-gateway/
├── shared/
│   └── contracts/
├── frontend/
├── infra/
│   └── docker-compose.yml
├── docs/
│   ├── ARCHITECTURE.md
│   └── CODING_GUIDELINES.md
├── scripts/
│   └── check.sh
├── Makefile
└── README.md
```

## Services

| Service | Purpose | App Module |
| --- | --- | --- |
| `knowledge-base` | Document system of record, positional chunks, search, citations, and chat history. | `kb.main:app` |
| `report-generator` | Report job orchestration scaffold with mock generate/read/download routes. | `reports.main:app` |
| `data-analytics` | Guarded NL2SQL scaffold with mock SQL generation and schema summary routes. | `analytics.main:app` |
| `assistant-gateway` | Optional conversational gateway with LangGraph routing. Keep only if the product needs one chat entry point. | `gateway.main:app` |

If your frontend already knows which service to call, `assistant-gateway` is optional and
can be removed later. The three direct services can work without it.

## Shared Contracts

`shared/contracts` defines cross-service Pydantic models:

- `ScopeObject`
- `DocumentMetadata`
- `Citation`
- `ChatMessage`

Services install it as a local path dependency using uv:

```toml
[tool.uv.sources]
contracts = { path = "../../shared/contracts", editable = true }
```

No business logic should go into `shared/contracts`.

## Local Development

Install dependencies inside a service:

```bash
cd services/knowledge-base
uv sync
cp .env.example .env
uv run uvicorn kb.main:app --reload
```

Run a service from the repo root:

```bash
make dev SERVICE=knowledge-base
make dev SERVICE=report-generator
make dev SERVICE=data-analytics
make dev SERVICE=assistant-gateway
```

## Quality Checks

Run checks for every service:

```bash
./scripts/check.sh
```

Or through Make:

```bash
make lint
make test
make check
```

The current scaffold has passing tests across all services.

## Docker

Run the local stack:

```bash
docker compose -f infra/docker-compose.yml up --build
```

The compose file starts Postgres with pgvector, Redis, and all service containers.

## Auth Model

Data-returning routes expect a JWT bearer token signed with `JWT_SECRET`. The token payload
is parsed into `ScopeObject` from `shared/contracts`.

Example payload:

```json
{
  "organization_uuid": "org-1",
  "user_uuid": "user-1",
  "user_email": "user@example.com",
  "role": "project_user",
  "project_uuids": ["project-a"]
}
```

The `knowledge-base` service enforces tenant/project filtering in the repository layer.

## Current Storage Defaults

The services use SQLite by default for local and test runs. Production settings are wired
through `DATABASE_URL` and are intended for PostgreSQL. The knowledge-base scaffold also
contains the pgvector column seam for embeddings.

MongoDB and PostGIS are not implemented yet. The recommended future direction is:

- PostgreSQL for system-of-record relational data.
- PostGIS as a PostgreSQL extension for geospatial data.
- MongoDB for flexible artifacts such as raw parser output, extraction traces, and report drafts.

## More Docs

- [Architecture](docs/ARCHITECTURE.md)
- [Coding Guidelines](docs/CODING_GUIDELINES.md)
- [LangChain LangGraph](docs/LANGCHAIN_LANGGRAPH.md)
