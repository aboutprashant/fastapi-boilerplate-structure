import pytest

from reports.orchestration.pipeline import ReportPipeline


@pytest.mark.asyncio
async def test_pipeline_returns_manifest() -> None:
    result = await ReportPipeline().run("summary")

    assert result["download_url"] == "/mock/report.pdf"
