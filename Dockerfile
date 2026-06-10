FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src ./src

RUN uv sync --frozen --no-dev

EXPOSE 8000

CMD ["/app/.venv/bin/uvicorn", "rag_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
