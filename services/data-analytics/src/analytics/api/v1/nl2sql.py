from fastapi import APIRouter

from analytics.core.auth import ScopeDep
from analytics.domain.schemas import NL2SQLRequest, NL2SQLResponse
from analytics.guards.sql_safety import validate_read_only
from analytics.orchestration.nl2sql import MockNL2SQL

router = APIRouter(prefix="/nl2sql", tags=["nl2sql"])


@router.post("/query", response_model=NL2SQLResponse)
async def query(payload: NL2SQLRequest, scope: ScopeDep) -> NL2SQLResponse:
    result = await MockNL2SQL().generate(payload.question, scope)
    warnings = [*result["warnings"], *validate_read_only(result["sql"])]
    return NL2SQLResponse(
        sql=result["sql"],
        rows=result["rows"],
        columns=result["columns"],
        warnings=warnings,
    )
