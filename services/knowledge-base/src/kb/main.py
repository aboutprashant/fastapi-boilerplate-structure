from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from kb.api.v1.health import router as health_router
from kb.api.v1.router import api_router
from kb.core.config import Settings, get_settings
from kb.core.errors import add_exception_handlers
from kb.core.logging import RequestLoggingMiddleware, configure_logging
from kb.persistence.database import create_engine_and_sessionmaker, create_schema, dispose_engine
from kb.retrieval.retriever import build_embedding_provider


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine, sessionmaker = create_engine_and_sessionmaker(settings.database_url)
        app.state.engine = engine
        app.state.sessionmaker = sessionmaker
        app.state.embedding_provider = build_embedding_provider(settings.use_mock_embeddings)
        await create_schema(engine)
        yield
        await dispose_engine(engine)

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
