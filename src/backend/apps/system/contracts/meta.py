from pydantic import BaseModel


class ServiceMetadata(BaseModel):
    service: str
    docs: str
    health: str
    liveness: str
    readiness: str


__all__ = ["ServiceMetadata"]
