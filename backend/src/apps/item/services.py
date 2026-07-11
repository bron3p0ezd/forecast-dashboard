from abc import abstractmethod
from datetime import date

from apps.item.schemas import ItemResponse, ItemRowsResponse, ItemsResponse
from settings.services import Service


class ItemService(Service):
    @abstractmethod
    async def get_item(
        self,
        sku: str,
    ) -> ItemResponse | None:
        ...

    @abstractmethod
    async def get_items(
        self,
        subcategory: str | None
    ) -> ItemsResponse:
        ...

    @abstractmethod
    async def get_item_rows(
        self,
        sku: str,
        date_from: date,
        date_to: date,
    ) -> ItemRowsResponse:
        ...
