from typing import Literal, Protocol

Intent = Literal["kb_lookup", "analytics", "report", "multi_doc_reasoning"]


class IntentClassifier(Protocol):
    async def classify(self, query: str) -> Intent:
        raise NotImplementedError


class MockIntentClassifier:
    async def classify(self, query: str) -> Intent:
        normalized = query.lower()
        if "report" in normalized or "generate" in normalized:
            return "report"
        if "sql" in normalized or "analytics" in normalized or "table" in normalized:
            return "analytics"
        if "donor" in normalized and ("progress" in normalized or "commitment" in normalized):
            return "multi_doc_reasoning"
        return "kb_lookup"
