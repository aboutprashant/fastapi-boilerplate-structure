from kb.ingestion.chunker import chunk_lines
from kb.ingestion.parsers.plain import parse_plain_text


def test_chunk_lines_keeps_line_positions() -> None:
    lines = parse_plain_text("line one\nline two")

    chunks = chunk_lines(lines, max_chars=100)

    assert chunks[0].page_number == 1
    assert chunks[0].line_start == 1
    assert chunks[0].line_end == 2
