from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.settings import get_settings

# The backend owns one process-level engine/session factory pair. They are
# module-scoped on purpose so runtime integrations and tests can share the same
# explicit singleton instead of constructing ad-hoc engines across imports.
settings = get_settings()

async_engine = create_async_engine(
    settings.db.postgres_dsn,
    future=True,
    pool_pre_ping=True,
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()


async def ping_database() -> None:
    async with async_engine.connect() as connection:
        await connection.execute(text("SELECT 1"))


__all__ = ["AsyncSessionLocal", "async_engine", "get_db_session", "ping_database"]
