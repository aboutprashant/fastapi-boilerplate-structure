from typing import Protocol

from contracts import Citation, ScopeObject

from gateway.agents.state import GatewayState
from gateway.agents.tools import PlatformTools
from gateway.router.intent import IntentClassifier


class AnswerSynthesizer(Protocol):
    async def synthesize(self, state: GatewayState) -> str:
        raise NotImplementedError


class MockAnswerSynthesizer:
    async def synthesize(self, state: GatewayState) -> str:
        intent = state.get("intent", "kb_lookup")
        if intent == "report":
            return (
                "I can hand this off to the report generator once required report "
                "inputs are confirmed."
            )
        if intent == "analytics":
            result = state.get("analytics_result", {})
            return f"Analytics result: {result.get('rows', [])}"
        context = " ".join(state.get("retrieved_context", []))
        return f"Based on platform context: {context[:700]}"


def classify_intent_node(classifier: IntentClassifier):
    async def classify_intent(state: GatewayState) -> GatewayState:
        query = _latest_user_message(state)
        intent = await classifier.classify(query)
        return {
            **state,
            "intent": intent,
            "route_trace": [*state.get("route_trace", []), "classify_intent"],
        }

    return classify_intent


def retrieve_simple_node(tools: PlatformTools):
    async def retrieve_simple(state: GatewayState) -> GatewayState:
        scope = _scope(state)
        contexts, citations = await tools.search_knowledge_base(_latest_user_message(state), scope)
        return {
            **state,
            "retrieved_context": contexts,
            "citations": [item.model_dump(mode="json") for item in citations],
            "route_trace": [*state.get("route_trace", []), "retrieve_simple"],
        }

    return retrieve_simple


async def plan_slots(state: GatewayState) -> GatewayState:
    query = _latest_user_message(state).lower()
    slots = ["donor_agreement", "me_plan", "progress_report"]
    if "evidence" in query:
        slots.append("indicator_evidence")
    return {**state, "slots": slots, "route_trace": [*state.get("route_trace", []), "plan_slots"]}


def retrieve_per_slot_node(tools: PlatformTools):
    async def retrieve_per_slot(state: GatewayState) -> GatewayState:
        scope = _scope(state)
        contexts: list[str] = []
        citations: list[Citation] = []
        for slot in state.get("slots", []):
            slot_contexts, slot_citations = await tools.search_knowledge_base(
                _latest_user_message(state),
                scope,
                doc_type=slot,
            )
            contexts.extend(slot_contexts)
            citations.extend(slot_citations)
        return {
            **state,
            "retrieved_context": contexts,
            "citations": [item.model_dump(mode="json") for item in citations],
            "route_trace": [*state.get("route_trace", []), "retrieve_per_slot"],
        }

    return retrieve_per_slot


def call_analytics_node(tools: PlatformTools):
    async def call_analytics(state: GatewayState) -> GatewayState:
        result = await tools.query_analytics(_latest_user_message(state), _scope(state))
        return {
            **state,
            "analytics_result": result,
            "route_trace": [*state.get("route_trace", []), "call_analytics"],
        }

    return call_analytics


def synthesize_node(synthesizer: AnswerSynthesizer):
    async def synthesize(state: GatewayState) -> GatewayState:
        answer = await synthesizer.synthesize(state)
        return {
            **state,
            "final_answer": answer,
            "route_trace": [*state.get("route_trace", []), "synthesize"],
        }

    return synthesize


def select_route(state: GatewayState) -> str:
    return state["intent"]


def _latest_user_message(state: GatewayState) -> str:
    return state["messages"][-1]["content"]


def _scope(state: GatewayState) -> ScopeObject:
    scope = state["scope"]
    if isinstance(scope, ScopeObject):
        return scope
    return ScopeObject.model_validate(scope)
