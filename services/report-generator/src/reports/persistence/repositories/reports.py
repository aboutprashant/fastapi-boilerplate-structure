from contracts import ScopeObject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from reports.core.errors import NotFoundError
from reports.persistence.models import ReportJob


class ReportRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_job(self, project_id: str, prompt: str, scope: ScopeObject) -> ReportJob:
        job = ReportJob(
            org_id=scope.organization_uuid,
            project_id=project_id,
            user_uuid=scope.user_uuid,
            scope_snapshot=scope.model_dump(),
            prompt=prompt,
            status="queued",
        )
        self.session.add(job)
        await self.session.flush()
        return job

    async def get_job(self, report_id: str, scope: ScopeObject) -> ReportJob:
        statement = select(ReportJob).where(
            ReportJob.id == report_id,
            ReportJob.org_id == scope.organization_uuid,
            ReportJob.project_id.in_(scope.project_uuids),
        )
        job = await self.session.scalar(statement)
        if job is None:
            raise NotFoundError("Report not found")
        return job
