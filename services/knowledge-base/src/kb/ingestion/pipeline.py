from contracts import ScopeObject
from sqlalchemy.ext.asyncio import AsyncSession

from kb.ingestion.chunker import chunk_lines
from kb.ingestion.classifier import MockDocumentClassifier
from kb.ingestion.parsers.plain import parse_plain_text
from kb.persistence.models import Chunk, Document
from kb.persistence.repositories.documents import DocumentRepository
from kb.retrieval.retriever import EmbeddingProvider


class IngestionPipeline:
    def __init__(
        self,
        session: AsyncSession,
        embedding_provider: EmbeddingProvider,
        classifier: MockDocumentClassifier | None = None,
    ) -> None:
        self.session = session
        self.embedding_provider = embedding_provider
        self.classifier = classifier or MockDocumentClassifier()

    async def ingest(self, document: Document, content: str, scope: ScopeObject) -> None:
        lines = parse_plain_text(content)
        chunks = chunk_lines(lines)
        repository = DocumentRepository(self.session)

        db_chunks = [
            Chunk(
                document_id=document.id,
                org_id=scope.organization_uuid,
                project_id=document.project_id,
                content=chunk.content,
                embedding=await self.embedding_provider.embed(chunk.content),
                page_number=chunk.page_number,
                line_start=chunk.line_start,
                line_end=chunk.line_end,
                char_start=chunk.char_start,
                char_end=chunk.char_end,
                metadata_json={
                    "source_context": document.source_context,
                    "doc_type": document.doc_type,
                },
            )
            for chunk in chunks
        ]
        await repository.add_chunks(db_chunks)

        first_pages_text = "\n".join(line.text for line in lines if line.page_number <= 10)
        classification = await self.classifier.classify(document.doc_type, first_pages_text)
        status = "active" if classification.verdict == "green" else "ingesting"
        await repository.set_classification(document.id, classification.verdict, status)
