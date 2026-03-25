from dataclasses import dataclass
from typing import Literal

from core.settings import Settings
from redis.exceptions import RedisError
from sqlalchemy.exc import SQLAlchemyError

from apps.system.contracts.health import DependencyProbe, LivenessProbe, ReadinessProbe
from apps.system.domain.ports import SystemHealthPort


@dataclass(slots=True, frozen=True)
class SystemStatusService:
    settings: Settings
    health_port: SystemHealthPort

    async def get_liveness(self) -> LivenessProbe:
        return LivenessProbe(service=self.settings.app.name)

    async def get_readiness(self) -> ReadinessProbe:
        checks: list[DependencyProbe] = []
        status: Literal["ok", "error"] = "ok"

        try:
            await self.health_port.ping_database()
        except OSError, SQLAlchemyError:
            status = "error"
            checks.append(DependencyProbe(name="postgres", status="error", detail="database unavailable"))
        else:
            checks.append(DependencyProbe(name="postgres", status="ok"))

        try:
            await self.health_port.ping_redis()
        except OSError, RedisError:
            status = "error"
            checks.append(DependencyProbe(name="redis", status="error", detail="redis unavailable"))
        else:
            checks.append(DependencyProbe(name="redis", status="ok"))

        return ReadinessProbe(status=status, service=self.settings.app.name, checks=tuple(checks))
