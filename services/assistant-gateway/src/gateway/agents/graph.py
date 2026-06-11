from langgraph.graph import END, StateGraph

from gateway.agents.nodes import (
    MockAnswerSynthesizer,
    call_analytics_node,
    classify_intent_node,
    plan_slots,
    retrieve_per_slot_node,
    retrieve_simple_node,
    select_route,
    synthesize_node,
)
from gateway.agents.state import GatewayState
from gateway.agents.tools import HTTPPlatformTools, MockPlatformTools
from gateway.core.config import Settings
from gateway.router.intent import MockIntentClassifier


def build_assistant_graph(settings: Settings):
    tools = (
        MockPlatformTools()
        if settings.use_mock_service_clients
        else HTTPPlatformTools(
            settings.knowledge_base_url,
            settings.data_analytics_url,
            settings.jwt_secret,
        )
    )
    classifier = MockIntentClassifier()
    synthesizer = MockAnswerSynthesizer()

    graph = StateGraph(GatewayState)
    graph.add_node("classify_intent", classify_intent_node(classifier))
    graph.add_node("retrieve_simple", retrieve_simple_node(tools))
    graph.add_node("plan_slots", plan_slots)
    graph.add_node("retrieve_per_slot", retrieve_per_slot_node(tools))
    graph.add_node("call_analytics", call_analytics_node(tools))
    graph.add_node("synthesize", synthesize_node(synthesizer))

    graph.set_entry_point("classify_intent")
    graph.add_conditional_edges(
        "classify_intent",
        select_route,
        {
            "kb_lookup": "retrieve_simple",
            "analytics": "call_analytics",
            "multi_doc_reasoning": "plan_slots",
            "report": "synthesize",
        },
    )
    graph.add_edge("retrieve_simple", "synthesize")
    graph.add_edge("call_analytics", "synthesize")
    graph.add_edge("plan_slots", "retrieve_per_slot")
    graph.add_edge("retrieve_per_slot", "synthesize")
    graph.add_edge("synthesize", END)
    return graph.compile()
