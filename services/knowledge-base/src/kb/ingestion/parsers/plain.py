from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedLine:
    page_number: int
    line_number: int
    char_start: int
    char_end: int
    text: str


def parse_plain_text(content: str) -> list[ParsedLine]:
    lines: list[ParsedLine] = []
    cursor = 0
    for index, line in enumerate(content.splitlines() or [content], start=1):
        start = cursor
        end = start + len(line)
        if line.strip():
            lines.append(
                ParsedLine(
                    page_number=1,
                    line_number=index,
                    char_start=start,
                    char_end=end,
                    text=line.strip(),
                )
            )
        cursor = end + 1
    return lines
