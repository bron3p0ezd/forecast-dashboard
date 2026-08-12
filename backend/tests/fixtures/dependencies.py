import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from apps.item.impls.repositories.daily_repository import DailyRepositoryImpl
from apps.item.impls.repositories.item_repository import ItemRepositoryImpl
from apps.item.impls.services.item_service import ItemServiceImpl


@pytest.fixture
def item_repository(session: AsyncSession) -> ItemRepositoryImpl:
    """Provide an item repository connected to the test database."""
    return ItemRepositoryImpl(session)


@pytest.fixture
def daily_repository(session: AsyncSession) -> DailyRepositoryImpl:
    """Provide a daily repository connected to the test database."""
    return DailyRepositoryImpl(session)


@pytest.fixture
def item_service(
    item_repository: ItemRepositoryImpl,
    daily_repository: DailyRepositoryImpl,
) -> ItemServiceImpl:
    """Provide an item service backed by the test database."""
    return ItemServiceImpl(
        repository=item_repository,
        daily_repository=daily_repository,
    )
