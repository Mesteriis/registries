from typing import Annotated

from core.bootstrap.system import build_system_status_service
from core.db.uow import BaseAsyncUnitOfWork, get_uow
from core.settings import Settings, get_settings
from fastapi import Depends

from apps.system.application.services import SystemStatusService

_UOW_DEP = Depends(get_uow)
_SETTINGS_DEP = Depends(get_settings)


def get_system_status_service(
    uow: BaseAsyncUnitOfWork = _UOW_DEP,
    settings: Settings = _SETTINGS_DEP,
) -> SystemStatusService:
    return build_system_status_service(settings=settings, uow=uow)


SystemStatusServiceDep = Annotated[SystemStatusService, Depends(get_system_status_service)]

__all__ = ["SystemStatusServiceDep", "get_system_status_service"]
