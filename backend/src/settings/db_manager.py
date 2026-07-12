from abc import ABC, abstractmethod
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession


class DbManager(ABC):
    @abstractmethod
    async def __aenter__(self) -> "DbManager": ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any
    ) -> None: ...

    @property
    @abstractmethod
    def session(self) -> AsyncSession: ...

    @abstractmethod
    async def commit(self) -> Any: ...

    @abstractmethod
    async def rollback(self) -> Any: ...
