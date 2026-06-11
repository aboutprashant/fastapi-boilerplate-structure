from pydantic import BaseModel, Field


class NL2SQLRequest(BaseModel):
    question: str = Field(..., min_length=1)


class NL2SQLResponse(BaseModel):
    sql: str
    rows: list[dict]
    columns: list[str]
    warnings: list[str]


class SchemaSummary(BaseModel):
    project_id: str
    tables: list[str]
    notes: str
