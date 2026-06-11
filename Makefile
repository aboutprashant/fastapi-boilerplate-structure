.PHONY: dev test lint check

SERVICES := knowledge-base report-generator data-analytics assistant-gateway
SERVICE ?= knowledge-base

dev:
	case "$(SERVICE)" in \
		knowledge-base) module="kb.main:app" ;; \
		report-generator) module="reports.main:app" ;; \
		data-analytics) module="analytics.main:app" ;; \
		assistant-gateway) module="gateway.main:app" ;; \
		*) echo "Unknown SERVICE=$(SERVICE)" && exit 1 ;; \
	esac; \
	cd services/$(SERVICE) && uv run uvicorn "$$module" --reload

test:
	for service in $(SERVICES); do cd services/$$service && uv run pytest && cd ../..; done

lint:
	for service in $(SERVICES); do cd services/$$service && uv run ruff check . && cd ../..; done

check: lint test
