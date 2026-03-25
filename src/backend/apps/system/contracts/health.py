from typing import Literal

from pydantic import BaseModel


class LivenessProbe(BaseModel):
    status: Literal["ok"] = "ok"
    service: str


class DependencyProbe(BaseModel):
    name: str
    status: Literal["ok", "error"]
    detail: str | None = None


class ReadinessProbe(BaseModel):
    status: Literal["ok", "error"]
    service: str
    checks: tuple[DependencyProbe, ...]


__all__ = ["DependencyProbe", "LivenessProbe", "ReadinessProbe"]
