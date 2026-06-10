import pytest

from rag_api.rag.chunking import chunk_text


def test_chunk_text_normalizes_whitespace() -> None:
    assert chunk_text("hello\n\nworld", chunk_size=20, overlap=2) == ["hello world"]


def test_chunk_text_rejects_invalid_overlap() -> None:
    with pytest.raises(ValueError):
        chunk_text("hello", chunk_size=10, overlap=10)
