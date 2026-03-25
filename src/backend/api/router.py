from apps.system.api import router as system_router
from fastapi import APIRouter


def build_router() -> APIRouter:
    router = APIRouter()
    v1_router = APIRouter(prefix="/v1")
    v1_router.include_router(system_router)
    router.include_router(v1_router)
    return router


api_router = build_router()
