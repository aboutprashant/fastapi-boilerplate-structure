from pydantic import BaseModel, Field


class ReportGenerateRequest(BaseModel):
    project_id: str
    prompt: str = Field(..., min_length=1)


class ReportGenerateResponse(BaseModel):
    report_id: str
    status: str


class ReportRead(BaseModel):
    report_id: str
    status: str
    project_id: str


class ReportDownloadResponse(BaseModel):
    report_id: str
    download_url: str
