import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from apps.item.impls.repositories.daily_repository import DailyRepositoryImpl
from apps.item.impls.repositories.item_repository import ItemRepositoryImpl


@pytest.fixture
def item_repository(session: AsyncSession) -> ItemRepositoryImpl:
    """Provide an item repository connected to the test database."""
    return ItemRepositoryImpl(session)


@pytest.fixture
def daily_repository(session: AsyncSession) -> DailyRepositoryImpl:
    """Provide a daily repository connected to the test database."""
    return DailyRepositoryImpl(session)
