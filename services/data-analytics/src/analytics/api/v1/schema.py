from fastapi import APIRouter

from analytics.core.auth import ScopeDep
from analytics.domain.schemas import SchemaSummary

router = APIRouter(prefix="/schema", tags=["schema"])


@router.get("/{project_id}", response_model=SchemaSummary)
async def get_schema(project_id: str, scope: ScopeDep) -> SchemaSummary:
    allowed = project_id in scope.project_uuids or scope.role == "org_admin"
    tables = ["project_metrics", "activities", "indicators"] if allowed else []
    return SchemaSummary(project_id=project_id, tables=tables, notes="Mock schema summary.")
