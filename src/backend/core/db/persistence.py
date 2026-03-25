from sqlalchemy.ext.asyncio import AsyncSession


class PersistenceComponent:
    def __init__(self, session: AsyncSession, *, component_name: str) -> None:
        self._session = session
        self._component_name = component_name

    @property
    def session(self) -> AsyncSession:
        return self._session

    @property
    def component_name(self) -> str:
        return self._component_name


class AsyncRepository(PersistenceComponent):
    def __init__(self, session: AsyncSession, *, repository_name: str) -> None:
        super().__init__(session, component_name=repository_name)


class AsyncQueryService(PersistenceComponent):
    def __init__(self, session: AsyncSession, *, service_name: str) -> None:
        super().__init__(session, component_name=service_name)


__all__ = ["AsyncQueryService", "AsyncRepository", "PersistenceComponent"]
