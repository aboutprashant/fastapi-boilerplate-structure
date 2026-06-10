from fastapi import APIRouter, Request

from rag_api.models.health import HealthResponse, ReadinessResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/ready", response_model=ReadinessResponse)
async def ready(request: Request) -> ReadinessResponse:
    checks = {"rag_service": hasattr(request.app.state, "rag_service")}
    return ReadinessResponse(status="ready" if all(checks.values()) else "not_ready", checks=checks)
