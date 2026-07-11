from typing import AsyncIterator

from settings.db_manager import DbManager
from settings.impls.sql_alchemy_manager import SQLAlchemyManager


async def get_sql_manager() -> AsyncIterator[DbManager]:
    async with SQLAlchemyManager() as uow:
        yield uow
