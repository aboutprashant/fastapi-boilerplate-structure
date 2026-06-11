from fastapi import APIRouter

from reports.api.v1 import reports

api_router = APIRouter()
api_router.include_router(reports.router)
