from fastapi import APIRouter

from kb.api.v1 import chat, documents, search

api_router = APIRouter()
api_router.include_router(documents.router)
api_router.include_router(search.router)
api_router.include_router(chat.router)
