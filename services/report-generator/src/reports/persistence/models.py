from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import JSON


def json_type() -> JSON:
    return JSON().with_variant(JSONB, "postgresql")


class Base(DeclarativeBase):
    pass


class ReportJob(Base):
    __tablename__ = "report_jobs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    org_id: Mapped[str] = mapped_column(String, index=True)
    project_id: Mapped[str] = mapped_column(String, index=True)
    user_uuid: Mapped[str] = mapped_column(String, index=True)
    scope_snapshot: Mapped[dict] = mapped_column(json_type())
    status: Mapped[str] = mapped_column(String, default="queued")
    prompt: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )


class ReportManifestRecord(Base):
    __tablename__ = "report_manifest_records"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    report_job_id: Mapped[str] = mapped_column(String, index=True)
    filename: Mapped[str] = mapped_column(String)
    content_type: Mapped[str] = mapped_column(String)
    storage_ref: Mapped[str] = mapped_column(String)
    manifest_json: Mapped[dict] = mapped_column(json_type(), default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
