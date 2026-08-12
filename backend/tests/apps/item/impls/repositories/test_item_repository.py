from apps.item.impls.repositories.item_repository import ItemRepositoryImpl
from apps.item.models import Item
from tests.fixtures.database_data import DatabaseData


async def test_select_item_by_sku_returns_matching_item(
    item_repository: ItemRepositoryImpl,
    database_data: DatabaseData,
) -> None:
    expected: Item = database_data.items.dairy

    actual: Item | None = await item_repository.select_item_by_sku(expected.item_id)

    assert actual is not None
    assert actual.item_id == expected.item_id
    assert actual.item_name == expected.item_name
    assert actual.subcategory == expected.subcategory


async def test_select_item_by_sku_returns_none_when_item_is_absent(
    item_repository: ItemRepositoryImpl,
    database_data: DatabaseData,
) -> None:
    existing_skus: set[str] = {item.item_id for item in database_data.items.all}
    absent_sku: str = "00-00000000"
    assert absent_sku not in existing_skus

    actual: Item | None = await item_repository.select_item_by_sku(absent_sku)

    assert actual is None


async def test_select_items_without_subcategory_returns_all_items(
    item_repository: ItemRepositoryImpl,
    database_data: DatabaseData,
) -> None:
    actual: list[Item] = await item_repository.select_items_by_subcategory(
        subcategory=None,
        limit=100,
        offset=0,
    )

    assert {item.item_id for item in actual} == {
        item.item_id for item in database_data.items.all
    }


async def test_select_items_orders_items_by_sku(
    item_repository: ItemRepositoryImpl,
    database_data: DatabaseData,
) -> None:
    expected_skus: list[str] = sorted(
        item.item_id for item in database_data.items.all
    )

    actual: list[Item] = await item_repository.select_items_by_subcategory(
        subcategory=None,
        limit=100,
        offset=0,
    )

    assert [item.item_id for item in actual] == expected_skus


async def test_select_items_applies_pagination(
    item_repository: ItemRepositoryImpl,
    database_data: DatabaseData,
) -> None:
    sorted_skus: list[str] = sorted(
        item.item_id for item in database_data.items.all
    )
    expected_skus: list[str] = sorted_skus[1:3]

    actual: list[Item] = await item_repository.select_items_by_subcategory(
        subcategory=None,
        limit=2,
        offset=1,
    )

    assert [item.item_id for item in actual] == expected_skus


async def test_select_items_filters_by_subcategory(
    item_repository: ItemRepositoryImpl,
    database_data: DatabaseData,
) -> None:
    expected: Item = database_data.items.bakery

    actual: list[Item] = await item_repository.select_items_by_subcategory(
        subcategory="Bakery",
        limit=100,
        offset=0,
    )

    assert expected.item_id in {item.item_id for item in actual}
    assert all("bakery" in item.subcategory.lower() for item in actual)


async def test_select_items_filters_subcategory_case_insensitively(
    item_repository: ItemRepositoryImpl,
    database_data: DatabaseData,
) -> None:
    expected: Item = database_data.items.extended_dairy

    actual: list[Item] = await item_repository.select_items_by_subcategory(
        subcategory="dairy",
        limit=100,
        offset=0,
    )

    assert expected.item_id in {item.item_id for item in actual}


async def test_select_items_filters_subcategory_by_partial_match(
    item_repository: ItemRepositoryImpl,
    database_data: DatabaseData,
) -> None:
    expected: Item = database_data.items.extended_dairy

    actual: list[Item] = await item_repository.select_items_by_subcategory(
        subcategory="Fresh",
        limit=100,
        offset=0,
    )

    assert [item.item_id for item in actual] == [expected.item_id]
