from datetime import date

import pytest

from apps.item.impls.repositories.daily_repository import DailyRepositoryImpl
from apps.item.models import Daily
from tests.fixtures.database_data import DatabaseData


async def test_select_item_rows_filters_by_sku(
    daily_repository: DailyRepositoryImpl,
    database_data: DatabaseData,
) -> None:
    selected_sku: str = database_data.items.forecast.item_id

    actual: list[Daily] = await daily_repository.select_item_rows(
        sku=selected_sku,
        date_from=date(2024, 12, 31),
        date_to=date(2025, 2, 1),
    )

    assert {row.item_id for row in actual} == {selected_sku}


@pytest.mark.parametrize(
    "boundary_date",
    [date(2025, 1, 1), date(2025, 1, 31)],
)
async def test_select_item_rows_includes_date_range_boundary(
    daily_repository: DailyRepositoryImpl,
    database_data: DatabaseData,
    boundary_date: date,
) -> None:
    actual: list[Daily] = await daily_repository.select_item_rows(
        sku=database_data.items.forecast.item_id,
        date_from=boundary_date,
        date_to=boundary_date,
    )

    assert [row.date for row in actual] == [boundary_date]


@pytest.mark.parametrize(
    "outside_date",
    [date(2024, 12, 31), date(2025, 2, 1)],
)
async def test_select_item_rows_excludes_date_outside_range(
    daily_repository: DailyRepositoryImpl,
    database_data: DatabaseData,
    outside_date: date,
) -> None:
    actual: list[Daily] = await daily_repository.select_item_rows(
        sku=database_data.items.forecast.item_id,
        date_from=date(2025, 1, 1),
        date_to=date(2025, 1, 31),
    )

    assert outside_date not in {row.date for row in actual}


async def test_select_item_rows_orders_rows_by_date(
    daily_repository: DailyRepositoryImpl,
    database_data: DatabaseData,
) -> None:
    expected_dates: list[date] = [
        date(2025, 1, 1),
        date(2025, 1, 15),
        date(2025, 1, 31),
    ]

    actual: list[Daily] = await daily_repository.select_item_rows(
        sku=database_data.items.forecast.item_id,
        date_from=date(2025, 1, 1),
        date_to=date(2025, 1, 31),
    )

    assert [row.date for row in actual] == expected_dates


async def test_select_item_rows_returns_empty_list_when_no_rows_match(
    daily_repository: DailyRepositoryImpl,
    database_data: DatabaseData,
) -> None:
    actual: list[Daily] = await daily_repository.select_item_rows(
        sku=database_data.items.forecast.item_id,
        date_from=date(2025, 3, 1),
        date_to=date(2025, 3, 31),
    )

    assert actual == []
