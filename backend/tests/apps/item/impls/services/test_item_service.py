from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from apps.item.enums import BiasDirection
from apps.item.exceptions import ItemNotFoundError
from apps.item.impls.services.item_service import ItemServiceImpl
from apps.item.models import Daily, Item
from tests.fixtures.database_data import DatabaseData


async def test_get_item_returns_item(
    item_service: ItemServiceImpl,
    database_data: DatabaseData,
) -> None:
    expected: Item = database_data.items.dairy

    actual = await item_service.get_item(expected.item_id)

    assert actual.sku == expected.item_id
    assert actual.name == expected.item_name
    assert actual.subcategory == expected.subcategory


async def test_get_item_raises_error_when_item_is_absent(
    item_service: ItemServiceImpl,
    database_data: DatabaseData,
) -> None:
    absent_sku = "00-00000000"
    assert absent_sku not in {item.item_id for item in database_data.items.all}

    with pytest.raises(ItemNotFoundError) as error:
        await item_service.get_item(absent_sku)

    assert error.value.sku == absent_sku


async def test_get_items_returns_page_and_reports_next_page(
    item_service: ItemServiceImpl,
    database_data: DatabaseData,
) -> None:
    expected_items = sorted(database_data.items.all, key=lambda item: item.item_id)[2:4]

    actual = await item_service.get_items(
        subcategory=None,
        page=2,
        page_size=2,
    )

    assert [item.sku for item in actual.items] == [
        item.item_id for item in expected_items
    ]
    assert actual.has_next is True


async def test_get_items_reports_last_page(
    item_service: ItemServiceImpl,
    database_data: DatabaseData,
) -> None:
    expected_items = sorted(database_data.items.all, key=lambda item: item.item_id)[4:]

    actual = await item_service.get_items(
        subcategory=None,
        page=3,
        page_size=2,
    )

    assert [item.sku for item in actual.items] == [
        item.item_id for item in expected_items
    ]
    assert actual.has_next is False


async def test_get_items_filters_by_subcategory(
    item_service: ItemServiceImpl,
    database_data: DatabaseData,
) -> None:
    expected_skus = {
        database_data.items.dairy.item_id,
        database_data.items.extended_dairy.item_id,
        database_data.items.forecast.item_id,
    }

    actual = await item_service.get_items(
        subcategory="dairy",
        page=1,
        page_size=10,
    )

    assert {item.sku for item in actual.items} == expected_skus
    assert actual.has_next is False


async def test_get_item_rows_returns_rows_in_requested_period(
    item_service: ItemServiceImpl,
    database_data: DatabaseData,
) -> None:
    actual = await item_service.get_item_rows(
        sku=database_data.items.forecast.item_id,
        date_from=date(2025, 1, 1),
        date_to=date(2025, 1, 31),
    )

    assert [row.date for row in actual.rows] == [
        date(2025, 1, 1),
        date(2025, 1, 15),
        date(2025, 1, 31),
    ]
    assert all(row.fact == row.ml for row in actual.rows)


async def test_get_item_rows_raises_error_when_item_is_absent(
    item_service: ItemServiceImpl,
    database_data: DatabaseData,
) -> None:
    absent_sku = "00-00000000"
    assert absent_sku not in {item.item_id for item in database_data.items.all}

    with pytest.raises(ItemNotFoundError) as error:
        await item_service.get_item_rows(
            sku=absent_sku,
            date_from=date(2025, 1, 1),
            date_to=date(2025, 1, 31),
        )

    assert error.value.sku == absent_sku


async def test_get_item_rows_calculates_metrics_using_manual_forecast(
    item_service: ItemServiceImpl,
    database_data: DatabaseData,
    session: AsyncSession,
) -> None:
    period_start: Daily = database_data.daily_rows.period_start
    inside_period: Daily = database_data.daily_rows.inside_period
    period_end: Daily = database_data.daily_rows.period_end
    period_start.ml = 18.0
    inside_period.ml = 5.0
    inside_period.ruki = 30.0
    period_end.ml = 40.0
    await session.flush()

    actual = await item_service.get_item_rows(
        sku=database_data.items.forecast.item_id,
        date_from=date(2025, 1, 1),
        date_to=date(2025, 1, 31),
    )

    assert actual.metrics.fa == 77.33
    assert actual.metrics.bias == 17.33
    assert actual.metrics.bias_direction is BiasDirection.UP


async def test_get_item_rows_reports_downward_bias(
    item_service: ItemServiceImpl,
    database_data: DatabaseData,
    session: AsyncSession,
) -> None:
    database_data.daily_rows.period_start.ml = 10.0
    database_data.daily_rows.inside_period.ml = 20.0
    database_data.daily_rows.period_end.ml = 25.0
    await session.flush()

    actual = await item_service.get_item_rows(
        sku=database_data.items.forecast.item_id,
        date_from=date(2025, 1, 1),
        date_to=date(2025, 1, 31),
    )

    assert actual.metrics.fa == 73.33
    assert actual.metrics.bias == 26.67
    assert actual.metrics.bias_direction is BiasDirection.DOWN


async def test_get_item_rows_ignores_rows_without_fact(
    item_service: ItemServiceImpl,
    database_data: DatabaseData,
    session: AsyncSession,
) -> None:
    database_data.daily_rows.period_start.ml = 0.0
    database_data.daily_rows.period_start.fact = None
    await session.flush()

    actual = await item_service.get_item_rows(
        sku=database_data.items.forecast.item_id,
        date_from=date(2025, 1, 1),
        date_to=date(2025, 1, 31),
    )

    assert actual.rows[0].fact is None
    assert actual.metrics.fa == 100.0
    assert actual.metrics.bias == 0.0
    assert actual.metrics.bias_direction is BiasDirection.UP


async def test_get_item_rows_returns_zero_metrics_when_period_has_no_rows(
    item_service: ItemServiceImpl,
    database_data: DatabaseData,
) -> None:
    actual = await item_service.get_item_rows(
        sku=database_data.items.forecast.item_id,
        date_from=date(2025, 3, 1),
        date_to=date(2025, 3, 31),
    )

    assert actual.rows == []
    assert actual.metrics.fa == 0.0
    assert actual.metrics.bias == 0.0
    assert actual.metrics.bias_direction is BiasDirection.UP
