from fastapi import FastAPI


def setup_metrics(app: FastAPI) -> None:
    try:
        from prometheus_fastapi_instrumentator import Instrumentator
    except ImportError:
        return

    Instrumentator(
        excluded_handlers=["/health", "/ready"],
        should_group_status_codes=True,
        should_ignore_untemplated=True,
    ).instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
