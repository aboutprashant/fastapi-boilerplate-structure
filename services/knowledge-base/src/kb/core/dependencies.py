from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    sessionmaker = request.app.state.sessionmaker
    async with sessionmaker() as session:
        session.info["embedding_provider"] = request.app.state.embedding_provider
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
