from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from kb.persistence.models import Base


def create_engine_and_sessionmaker(database_url: str) -> tuple[AsyncEngine, async_sessionmaker]:
    engine = create_async_engine(database_url, future=True)
    return engine, async_sessionmaker(engine, expire_on_commit=False)


async def create_schema(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def check_database(engine: AsyncEngine) -> bool:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


async def dispose_engine(engine: AsyncEngine) -> None:
    await engine.dispose()


async def session_scope(sessionmaker: async_sessionmaker) -> AsyncIterator:
    async with sessionmaker() as session:
        yield session
