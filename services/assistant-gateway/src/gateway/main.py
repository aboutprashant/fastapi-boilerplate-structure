from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from gateway.agents.graph import build_assistant_graph
from gateway.api.v1.health import router as health_router
from gateway.api.v1.router import api_router
from gateway.core.config import Settings, get_settings
from gateway.core.errors import add_exception_handlers
from gateway.core.logging import RequestLoggingMiddleware, configure_logging


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.settings = settings
        app.state.assistant_graph = build_assistant_graph(settings)
        yield

    app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
    app.dependency_overrides[get_settings] = lambda: settings
    app.add_middleware(RequestLoggingMiddleware)
    add_exception_handlers(app)
    Instrumentator(excluded_handlers=["/health", "/ready"]).instrument(app).expose(
        app,
        endpoint="/metrics",
        include_in_schema=False,
    )
    app.include_router(health_router)
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
