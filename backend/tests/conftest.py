import os
from collections.abc import AsyncIterator, Iterator
from pathlib import Path
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


os.environ.setdefault("DB_PATH", "test.db")

from settings.database import Base
from tests.fixtures.dependencies import (  # noqa: E402, F401
    daily_repository,
    item_repository,
)
from tests.fixtures.database_data import (  # noqa: E402, F401
    database_data,
    daily_factory,
    item_factory,
)


@pytest.fixture
def database_path() -> Iterator[Path]:
    """Provide a unique SQLite file path and remove the file after the test."""
    database_directory: Path = Path(__file__).resolve().parent / ".databases"
    database_directory.mkdir(exist_ok=True)
    path: Path = database_directory / f"{uuid4().hex}.sqlite3"

    yield path

    path.unlink(missing_ok=True)


@pytest_asyncio.fixture
async def engine(database_path: Path) -> AsyncIterator[AsyncEngine]:
    """Create and dispose an asynchronous SQLite engine."""
    database_engine: AsyncEngine = create_async_engine(
        f"sqlite+aiosqlite:///{database_path.as_posix()}"
    )

    yield database_engine

    await database_engine.dispose()


@pytest_asyncio.fixture
async def database_schema(engine: AsyncEngine) -> AsyncIterator[None]:
    """Create the application schema and drop it after the test."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session_factory(
    engine: AsyncEngine,
    database_schema: None,
) -> async_sessionmaker[AsyncSession]:
    """Build a session factory for the prepared test database."""
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    """Open and close one database session for a test."""
    async with session_factory() as database_session:
        yield database_session
