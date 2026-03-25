from pydantic import BaseModel


class ServiceHealth(BaseModel):
    status: str
    service: str
