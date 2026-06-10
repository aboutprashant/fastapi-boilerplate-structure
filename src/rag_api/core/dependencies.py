from fastapi import Request

from rag_api.services.rag_service import RagService


def get_rag_service(request: Request) -> RagService:
    return request.app.state.rag_service
