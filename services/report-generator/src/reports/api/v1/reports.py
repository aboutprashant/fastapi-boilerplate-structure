from fastapi import APIRouter

from reports.core.auth import ScopeDep
from reports.core.dependencies import SessionDep
from reports.domain.schemas import (
    ReportDownloadResponse,
    ReportGenerateRequest,
    ReportGenerateResponse,
    ReportRead,
)
from reports.orchestration.pipeline import ReportPipeline
from reports.persistence.repositories.reports import ReportRepository

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/generate", response_model=ReportGenerateResponse)
async def generate_report(
    payload: ReportGenerateRequest,
    session: SessionDep,
    scope: ScopeDep,
) -> ReportGenerateResponse:
    job = await ReportRepository(session).create_job(payload.project_id, payload.prompt, scope)
    await ReportPipeline().run(payload.prompt)
    await session.commit()
    return ReportGenerateResponse(report_id=job.id, status=job.status)


@router.get("/{report_id}", response_model=ReportRead)
async def get_report(report_id: str, session: SessionDep, scope: ScopeDep) -> ReportRead:
    job = await ReportRepository(session).get_job(report_id, scope)
    return ReportRead(report_id=job.id, status=job.status, project_id=job.project_id)


@router.get("/{report_id}/download", response_model=ReportDownloadResponse)
async def download_report(
    report_id: str,
    session: SessionDep,
    scope: ScopeDep,
) -> ReportDownloadResponse:
    job = await ReportRepository(session).get_job(report_id, scope)
    return ReportDownloadResponse(report_id=job.id, download_url=f"/downloads/{job.id}.pdf")
