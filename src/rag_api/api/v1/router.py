from fastapi import APIRouter

from rag_api.api.v1 import rag

api_router = APIRouter()
api_router.include_router(rag.router, prefix="/rag", tags=["rag"])
