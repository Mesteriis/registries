from fastapi import APIRouter

from apps.system.api.read_endpoints import router as read_router

router = APIRouter(prefix="/system")
router.include_router(read_router)
