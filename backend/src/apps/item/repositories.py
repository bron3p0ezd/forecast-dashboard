from abc import abstractmethod

from apps.item.models import Item
from settings.repositories import Repository


class ItemRepository(Repository):
    @abstractmethod
    async def select_items_by_subcategory(
        self,
        subcategory: str | None,
    ) -> list[Item]:
        ...
