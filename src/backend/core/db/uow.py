from collections.abc import AsyncIterator
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import AsyncSessionLocal


class BaseAsyncUnitOfWork(AbstractAsyncContextManager["BaseAsyncUnitOfWork"]):
    """Explicit-commit async unit of work.

    Persistence is never committed implicitly on context exit. Call ``commit()``
    inside the context when work should be persisted. If the context exits
    without an explicit commit, any still-open transaction is rolled back.
    """

    def __init__(self, session: AsyncSession, *, owns_session: bool) -> None:
        self._session = session
        self._owns_session = owns_session

    @property
    def session(self) -> AsyncSession:
        return self._session

    async def __aenter__(self) -> BaseAsyncUnitOfWork:
        return self

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def flush(self) -> None:
        await self._session.flush()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        _exc_value: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:
        # Roll back on both error exit and "silent success without commit".
        # This keeps transaction ownership obvious at the call site.
        if exc_type is None and self._transaction_is_open():
            await self._session.rollback()
        if exc_type is not None:
            await self._session.rollback()
        if self._owns_session:
            await self._session.close()

    def _transaction_is_open(self) -> bool:
        in_transaction = getattr(self._session, "in_transaction", None)
        if callable(in_transaction):
            return bool(in_transaction())
        return False


class AsyncUnitOfWork(BaseAsyncUnitOfWork):
    def __init__(self) -> None:
        super().__init__(AsyncSessionLocal(), owns_session=True)


class SessionUnitOfWork(BaseAsyncUnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, owns_session=False)


async def get_uow() -> AsyncIterator[BaseAsyncUnitOfWork]:
    async with AsyncUnitOfWork() as uow:
        yield uow


@asynccontextmanager
async def async_session_scope() -> AsyncIterator[AsyncSession]:
    """Yield the underlying session with the same rollback-on-exit semantics."""
    async with AsyncUnitOfWork() as uow:
        yield uow.session


__all__ = [
    "AsyncUnitOfWork",
    "BaseAsyncUnitOfWork",
    "SessionUnitOfWork",
    "async_session_scope",
    "get_uow",
]
