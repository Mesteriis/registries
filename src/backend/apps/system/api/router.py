from fastapi import APIRouter

from apps.system.application.services import get_service_health
from apps.system.contracts.health import ServiceHealth

router = APIRouter(tags=["system"])


@router.get("/health", response_model=ServiceHealth)
async def read_health() -> ServiceHealth:
    return get_service_health()
