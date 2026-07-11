from apps.item.services import ItemService
from apps.item.repositories import ItemRepository
from apps.item.schemas import ItemResponse, ItemsResponse
from apps.item.models import Item


class ItemServiceImpl(ItemService):
    def __init__(
        self,
        repository: ItemRepository,
    ) -> None:
        self.__repository = repository

    async def get_items(
        self,
        subcategory: str | None
    ) -> ItemsResponse:
        items = await self.__repository.select_items_by_subcategory(subcategory)

        return self.__build_items_response(items)
        
    def __build_items_response(
        self,
        items: list[Item],
    ) -> ItemsResponse:
        return ItemsResponse(
            items=[
                ItemResponse(
                    sku=item.item_id,
                    name=item.item_name,
                    subcategory=item.subcategory,
                )
                for item in items
            ]
        )
