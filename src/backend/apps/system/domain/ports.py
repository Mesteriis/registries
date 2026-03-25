from typing import Protocol


class SystemHealthPort(Protocol):
    async def ping_database(self) -> None: ...

    async def ping_redis(self) -> None: ...


__all__ = ["SystemHealthPort"]
