from contracts import Citation

from kb.persistence.models import Chunk, Document


def build_citation(chunk: Chunk, document: Document) -> Citation:
    return Citation(
        document_id=document.id,
        title=document.name,
        doc_type=document.doc_type,
        version_date=document.version_date,
        page=chunk.page_number,
        line_start=chunk.line_start,
        line_end=chunk.line_end,
        quote=chunk.content[:500],
        link=f"/documents/{document.id}/view#page={chunk.page_number}",
    )
