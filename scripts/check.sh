#!/usr/bin/env bash
set -euo pipefail

services=(
  "knowledge-base"
  "report-generator"
  "data-analytics"
  "assistant-gateway"
)

for service in "${services[@]}"; do
  echo "==> $service"
  pushd "services/$service" >/dev/null
  uv run ruff check .
  uv run pytest
  popd >/dev/null
done
