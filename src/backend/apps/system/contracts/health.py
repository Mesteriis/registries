from typing import Literal

from pydantic import BaseModel, ConfigDict


class LivenessProbe(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"]
    service: str


class DependencyProbe(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    status: Literal["ok", "error"]
    detail: str | None = None


class ReadinessProbe(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["ok", "error"]
    service: str
    checks: tuple[DependencyProbe, ...]


__all__ = ["DependencyProbe", "LivenessProbe", "ReadinessProbe"]
