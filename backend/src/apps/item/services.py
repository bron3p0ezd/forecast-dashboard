from abc import abstractmethod

from apps.item.schemas import ItemsResponse
from settings.services import Service


class ItemService(Service):
    @abstractmethod
    async def get_items(
        self,
        subcategory: str | None
    ) -> ItemsResponse:
        ...
