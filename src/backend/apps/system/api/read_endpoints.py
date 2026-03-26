from typing import Any

from fastapi import APIRouter, Response, status

from apps.system.api.deps import SystemStatusServiceDep
from apps.system.api.errors import system_error_responses
from apps.system.contracts.health import LivenessProbe, ReadinessProbe

router = APIRouter(tags=["system:read"])
_READINESS_UNAVAILABLE_RESPONSE: dict[int | str, dict[str, Any]] = {
    status.HTTP_503_SERVICE_UNAVAILABLE: {
        "model": ReadinessProbe,
        "description": "One or more dependency checks failed.",
    }
}


@router.get("/livez", response_model=LivenessProbe, responses=system_error_responses(500))
async def read_liveness(service: SystemStatusServiceDep) -> LivenessProbe:
    return await service.get_liveness()


@router.get(
    "/readyz",
    response_model=ReadinessProbe,
    responses={**system_error_responses(500), **_READINESS_UNAVAILABLE_RESPONSE},
)
async def read_readiness(response: Response, service: SystemStatusServiceDep) -> ReadinessProbe:
    readiness = await service.get_readiness()
    if readiness.status != "ok":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return readiness


@router.get(
    "/health",
    response_model=ReadinessProbe,
    responses={**system_error_responses(500), **_READINESS_UNAVAILABLE_RESPONSE},
)
async def read_health(response: Response, service: SystemStatusServiceDep) -> ReadinessProbe:
    readiness = await service.get_readiness()
    if readiness.status != "ok":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return readiness
