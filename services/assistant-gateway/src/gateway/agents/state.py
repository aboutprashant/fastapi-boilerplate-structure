from typing import Any, Literal, TypedDict

from contracts import Citation, ScopeObject

Intent = Literal["kb_lookup", "analytics", "report", "multi_doc_reasoning"]


class GatewayState(TypedDict, total=False):
    messages: list[dict[str, str]]
    scope: ScopeObject | dict[str, Any]
    intent: Intent
    slots: list[str]
    retrieved_context: list[str]
    citations: list[Citation | dict[str, Any]]
    final_answer: str
    route_trace: list[str]
    analytics_result: dict[str, Any]
