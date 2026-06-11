# ai-platform Architecture

This repository is a monorepo of standalone services. Every directory under `services/`
is a complete FastAPI application with its own dependency graph, lockfile, Dockerfile,
tests, and environment configuration.

Services communicate over HTTP only. They do not import code from each other. The only
shared Python package is `shared/contracts`, which contains Pydantic schemas and no
business logic.

Chat request flow:

```text
Client
  |
  v
assistant-gateway /api/v1/chat
  |
  +--> classify intent
  |
  +--> knowledge-base /api/v1/search       (document retrieval)
  |
  +--> data-analytics /api/v1/nl2sql/query (analytics intent)
  |
  +--> report-generator /api/v1/reports/generate (report generation intent)
  v
synthesize answer with citations
  |
  v
Client
```

