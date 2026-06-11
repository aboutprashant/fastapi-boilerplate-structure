from typing import Protocol

from arq.connections import RedisSettings
from contracts import ScopeObject
from sqlalchemy.ext.asyncio import AsyncSession

from kb.ingestion.pipeline import IngestionPipeline
from kb.persistence.models import Document
from kb.retrieval.retriever import EmbeddingProvider


class IngestionQueue(Protocol):
    async def enqueue(
        self,
        session: AsyncSession,
        document: Document,
        content: str,
        scope: ScopeObject,
        embedding_provider: EmbeddingProvider,
    ) -> None:
        raise NotImplementedError


class LocalIngestionQueue:
    """Local deterministic queue seam; production can swap this for arq enqueueing."""

    async def enqueue(
        self,
        session: AsyncSession,
        document: Document,
        content: str,
        scope: ScopeObject,
        embedding_provider: EmbeddingProvider,
    ) -> None:
        await IngestionPipeline(session, embedding_provider=embedding_provider).ingest(
            document,
            content,
            scope,
        )


async def ingest_document_task(ctx: dict, document_id: str) -> str:
    return f"ingestion-scheduled:{document_id}"


class WorkerSettings:
    functions = [ingest_document_task]
    redis_settings = RedisSettings()
