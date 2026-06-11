from fastapi import APIRouter, Request

from kb.persistence.database import check_database

router = APIRouter(tags=["system"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def ready(request: Request) -> dict[str, object]:
    database = await check_database(request.app.state.engine)
    return {"status": "ready" if database else "not_ready", "checks": {"database": database}}
