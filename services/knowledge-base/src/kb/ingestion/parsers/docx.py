from kb.ingestion.parsers.plain import ParsedLine


def parse_docx(path: str) -> list[ParsedLine]:
    from docx import Document

    document = Document(path)
    content = "\n".join(paragraph.text for paragraph in document.paragraphs)
    from kb.ingestion.parsers.plain import parse_plain_text

    return parse_plain_text(content)
