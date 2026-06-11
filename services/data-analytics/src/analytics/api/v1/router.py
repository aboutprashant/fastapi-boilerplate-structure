from fastapi import APIRouter

from analytics.api.v1 import nl2sql, schema

api_router = APIRouter()
api_router.include_router(nl2sql.router)
api_router.include_router(schema.router)
