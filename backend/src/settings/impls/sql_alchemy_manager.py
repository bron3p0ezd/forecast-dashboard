from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from settings.database import async_session_maker
from settings.db_manager import DbManager


class SQLAlchemyManager(DbManager):
    def __init__(self):
        self.session_factory = async_session_maker
        self._session: Optional[AsyncSession] = None

    async def __aenter__(self) -> "SQLAlchemyManager":
        self._session = self.session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any
    ):
        if self._session is None:
            return

        if exc_type is not None:
            await self.rollback()
        await self._session.close()

    @property
    def session(self) -> AsyncSession:
        assert self._session is not None, "session доступен только внутри 'async with'"

        return self._session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
