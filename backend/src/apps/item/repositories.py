from abc import abstractmethod
from datetime import date

from apps.item.models import Daily, Item
from settings.repositories import Repository


class ItemRepository(Repository):
    @abstractmethod
    async def select_items_by_subcategory(
        self,
        subcategory: str | None,
    ) -> list[Item]:
        ...


class DailyRepository(Repository):
    @abstractmethod
    async def select_item_rows(
        self,
        sku: str,
        date_from: date,
        date_to: date,
    ) -> list[Daily]:
        ...
