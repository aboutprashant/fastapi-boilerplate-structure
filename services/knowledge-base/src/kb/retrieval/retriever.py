import hashlib
import math
import re
from typing import Protocol


class EmbeddingProvider(Protocol):
    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError


class VectorSearch(Protocol):
    async def search(self, query: str, top_k: int) -> list[str]:
        raise NotImplementedError


class HashEmbeddingProvider:
    def __init__(self, dimensions: int = 128) -> None:
        self.dimensions = dimensions

    async def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in re.findall(r"\w+", text.lower()):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            vector[index] += 1.0 if digest[4] % 2 == 0 else -1.0
        norm = math.sqrt(sum(value * value for value in vector))
        return vector if norm == 0 else [value / norm for value in vector]


def build_embedding_provider(use_mock: bool) -> EmbeddingProvider:
    if not use_mock:
        return HashEmbeddingProvider()
    return HashEmbeddingProvider()
