from apps.system.application.services import SystemStatusService
from apps.system.infrastructure.repositories import SystemHealthRepository

from core.db.uow import BaseAsyncUnitOfWork
from core.settings import Settings


def build_system_status_service(*, settings: Settings, uow: BaseAsyncUnitOfWork) -> SystemStatusService:
    return SystemStatusService(
        settings=settings,
        health_port=SystemHealthRepository(uow.session, redis_url=settings.db.redis_url),
    )


__all__ = ["build_system_status_service"]
