from datetime import date
from typing import Protocol

from apps.item.models import Daily, Item


class ItemFactory(Protocol):
    def __call__(self, sku: str, name: str, subcategory: str) -> Item: ...


class DailyFactory(Protocol):
    def __call__(self, sku: str, row_date: date, fact: float) -> Daily: ...


def make_item(sku: str, name: str, subcategory: str) -> Item:
    return Item(
        item_id=sku,
        item_name=name,
        subcategory=subcategory,
    )


def make_daily(sku: str, row_date: date, fact: float) -> Daily:
    return Daily(
        item_id=sku,
        date=row_date,
        fact=fact,
        sales=fact,
        math=fact,
        ml=fact,
        ruki=None,
    )
