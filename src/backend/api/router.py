from apps.system.api import router as system_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(system_router, prefix="/system")
