from contracts import Citation
from fastapi import APIRouter
from pydantic import BaseModel, Field

from gateway.core.auth import ScopeDep
from gateway.core.dependencies import AssistantGraphDep

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    answer: str
    intent: str
    citations: list[Citation] = []


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    scope: ScopeDep,
    assistant_graph: AssistantGraphDep,
) -> ChatResponse:
    state = await assistant_graph.ainvoke(
        {
            "messages": [{"role": "user", "content": payload.message}],
            "scope": scope.model_dump(),
            "route_trace": [],
        }
    )
    return ChatResponse(
        answer=state["final_answer"],
        intent=state["intent"],
        citations=[Citation.model_validate(item) for item in state.get("citations", [])],
    )
