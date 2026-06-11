# Coding Guidelines

- Each service must remain standalone and runnable in isolation.
- Services must not import Python modules from other services.
- Shared contracts must contain Pydantic schemas only.
- FastAPI route modules should stay thin; business logic belongs in orchestration,
  domain, retrieval, generation, or persistence modules.
- All database access must go through `persistence/repositories/`.
- Use async SQLAlchemy 2.x for database IO where a database is present.
- Use repository-layer tenancy filters, not route-layer tenancy filters.
- Data-returning routes must require JWT auth and operate from `ScopeObject`.
- Do not store raw auth tokens in any database table.
- Use deterministic mock providers by default so tests run offline.
- Keep LangChain and LangGraph usage limited to `services/assistant-gateway`.
- Use `uv`, `ruff`, and `pytest` in every service.
