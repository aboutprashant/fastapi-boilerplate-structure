from gateway.agents.graph import build_assistant_graph
from gateway.core.config import Settings


async def test_progress_query_routes_through_multi_doc_path() -> None:
    graph = build_assistant_graph(Settings(environment="test"))
    state = await graph.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "How is my project progressing against donor commitments?",
                }
            ],
            "scope": {
                "organization_uuid": "org-1",
                "user_uuid": "user-1",
                "user_email": "user@example.com",
                "role": "project_user",
                "project_uuids": ["project-a"],
            },
            "route_trace": [],
        }
    )

    assert state["intent"] == "multi_doc_reasoning"
    assert state["route_trace"] == [
        "classify_intent",
        "plan_slots",
        "retrieve_per_slot",
        "synthesize",
    ]
    assert state["slots"] == ["donor_agreement", "me_plan", "progress_report"]
