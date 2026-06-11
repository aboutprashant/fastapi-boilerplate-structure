from kb.persistence.models import Chunk, Document


def assemble_context(chunk: Chunk, document: Document) -> str:
    header = (
        f"[Doc: {document.name} | Type: {document.doc_type} | "
        f"Version: {document.version_date.isoformat()} | Page {chunk.page_number}]"
    )
    return f"{header}\n{chunk.content}"
