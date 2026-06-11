from dataclasses import dataclass

from kb.ingestion.parsers.plain import ParsedLine


@dataclass(frozen=True)
class PositionalChunk:
    content: str
    page_number: int
    line_start: int
    line_end: int
    char_start: int
    char_end: int


def chunk_lines(lines: list[ParsedLine], max_chars: int = 900) -> list[PositionalChunk]:
    chunks: list[PositionalChunk] = []
    current: list[ParsedLine] = []
    current_size = 0

    for line in lines:
        next_size = current_size + len(line.text) + 1
        if current and next_size > max_chars:
            chunks.append(_build_chunk(current))
            current = []
            current_size = 0
        current.append(line)
        current_size += len(line.text) + 1

    if current:
        chunks.append(_build_chunk(current))
    return chunks


def _build_chunk(lines: list[ParsedLine]) -> PositionalChunk:
    first = lines[0]
    last = lines[-1]
    return PositionalChunk(
        content="\n".join(line.text for line in lines),
        page_number=first.page_number,
        line_start=first.line_number,
        line_end=last.line_number,
        char_start=first.char_start,
        char_end=last.char_end,
    )
