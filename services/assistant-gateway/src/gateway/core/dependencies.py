from typing import Annotated, Any

from fastapi import Depends, Request


def get_assistant_graph(request: Request) -> Any:
    return request.app.state.assistant_graph


AssistantGraphDep = Annotated[Any, Depends(get_assistant_graph)]
