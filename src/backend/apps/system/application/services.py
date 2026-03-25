from core.settings import get_settings

from apps.system.contracts.health import ServiceHealth


def get_service_health() -> ServiceHealth:
    settings = get_settings()
    return ServiceHealth(status="ok", service=settings.app_name)
