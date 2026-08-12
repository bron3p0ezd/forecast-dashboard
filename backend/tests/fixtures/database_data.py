from dataclasses import dataclass
from datetime import date

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from apps.item.models import Daily, Item
from tests.fixtures.factories import DailyFactory, ItemFactory, make_daily, make_item


@dataclass(frozen=True, slots=True)
class ItemData:
    dairy: Item
    bakery: Item
    extended_dairy: Item
    food: Item
    forecast: Item
    other_forecast: Item

    @property
    def all(self) -> tuple[Item, ...]:
        return (
            self.dairy,
            self.bakery,
            self.extended_dairy,
            self.food,
            self.forecast,
            self.other_forecast,
        )


@dataclass(frozen=True, slots=True)
class DailyData:
    before_period: Daily
    period_start: Daily
    inside_period: Daily
    period_end: Daily
    after_period: Daily
    other_item: Daily

    @property
    def all(self) -> tuple[Daily, ...]:
        return (
            self.before_period,
            self.period_start,
            self.inside_period,
            self.period_end,
            self.after_period,
            self.other_item,
        )


@dataclass(frozen=True, slots=True)
class DatabaseData:
    items: ItemData
    daily_rows: DailyData


@pytest.fixture
def item_factory() -> ItemFactory:
    """Provide a reusable item test-data factory."""
    return make_item


@pytest.fixture
def daily_factory() -> DailyFactory:
    """Provide a reusable daily-row test-data factory."""
    return make_daily


@pytest_asyncio.fixture
async def database_data(
    session: AsyncSession,
    item_factory: ItemFactory,
    daily_factory: DailyFactory,
) -> DatabaseData:
    """Insert and expose the shared application integration-test dataset."""
    items: ItemData = ItemData(
        dairy=item_factory("01-00000001", "Milk", "Dairy"),
        bakery=item_factory("01-00000002", "Bread", "Bakery"),
        extended_dairy=item_factory(
            "01-00000003",
            "Yogurt",
            "Fresh DAIRY Products",
        ),
        food=item_factory("01-00000004", "Apple", "Food"),
        forecast=item_factory("12-12345678", "Cream", "Dairy"),
        other_forecast=item_factory("34-87654321", "Bun", "Bakery"),
    )
    daily_rows: DailyData = DailyData(
        before_period=daily_factory(
            items.forecast.item_id,
            date(2024, 12, 31),
            10.0,
        ),
        period_start=daily_factory(
            items.forecast.item_id,
            date(2025, 1, 1),
            20.0,
        ),
        inside_period=daily_factory(
            items.forecast.item_id,
            date(2025, 1, 15),
            25.0,
        ),
        period_end=daily_factory(
            items.forecast.item_id,
            date(2025, 1, 31),
            30.0,
        ),
        after_period=daily_factory(
            items.forecast.item_id,
            date(2025, 2, 1),
            40.0,
        ),
        other_item=daily_factory(
            items.other_forecast.item_id,
            date(2025, 1, 15),
            50.0,
        ),
    )
    data: DatabaseData = DatabaseData(items=items, daily_rows=daily_rows)

    async with session.begin():
        session.add_all(data.items.all)
        await session.flush()
        session.add_all(data.daily_rows.all)

    return data
