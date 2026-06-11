from fastapi import APIRouter, Request

router = APIRouter(tags=["system"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def ready(request: Request) -> dict[str, object]:
    graph_ready = hasattr(request.app.state, "assistant_graph")
    return {"status": "ready" if graph_ready else "not_ready", "checks": {"graph": graph_ready}}
