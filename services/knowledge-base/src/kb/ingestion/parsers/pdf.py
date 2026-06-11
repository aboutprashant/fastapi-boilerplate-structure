from kb.ingestion.parsers.plain import ParsedLine


def parse_pdf(path: str) -> list[ParsedLine]:
    import fitz

    lines: list[ParsedLine] = []
    with fitz.open(path) as document:
        for page_index, page in enumerate(document, start=1):
            cursor = 0
            for line_index, line in enumerate(page.get_text().splitlines(), start=1):
                start = cursor
                end = start + len(line)
                if line.strip():
                    lines.append(ParsedLine(page_index, line_index, start, end, line.strip()))
                cursor = end + 1
    return lines
