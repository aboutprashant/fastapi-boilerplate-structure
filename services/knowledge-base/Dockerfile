FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

COPY services/knowledge-base/pyproject.toml services/knowledge-base/uv.lock services/knowledge-base/README.md ./
COPY shared/contracts /shared/contracts
COPY services/knowledge-base/src ./src
RUN uv sync --frozen --no-dev

FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN useradd --create-home --shell /usr/sbin/nologin appuser
COPY --from=builder /app/.venv /app/.venv
COPY services/knowledge-base/src ./src

USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD /app/.venv/bin/python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["/app/.venv/bin/uvicorn", "kb.main:app", "--host", "0.0.0.0", "--port", "8000"]
