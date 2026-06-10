.PHONY: install dev test lint check docker-up

install:
	uv sync

dev:
	uv run uvicorn rag_api.main:app --reload

test:
	uv run pytest

lint:
	uv run ruff check .

check: lint test

docker-up:
	docker compose up --build
