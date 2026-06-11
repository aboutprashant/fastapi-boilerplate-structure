from typing import Protocol

from contracts import Citation


class AnswerGenerator(Protocol):
    async def generate(self, question: str, contexts: list[str], citations: list[Citation]) -> str:
        raise NotImplementedError


class ExtractiveMockAnswerGenerator:
    async def generate(self, question: str, contexts: list[str], citations: list[Citation]) -> str:
        if not contexts:
            return "No relevant context was found."
        return "Based on the retrieved documents: " + " ".join(contexts)[:700]


def build_answer_generator(use_mock: bool) -> AnswerGenerator:
    if not use_mock:
        return ExtractiveMockAnswerGenerator()
    return ExtractiveMockAnswerGenerator()
