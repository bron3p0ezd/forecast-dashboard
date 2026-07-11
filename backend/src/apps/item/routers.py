from fastapi import APIRouter, Depends, Query

from apps.item.schemas import ItemsResponse
from apps.item.services import ItemService
from apps.item.dependencies import get_item_service


router = APIRouter(
    prefix="/items",
    tags=["Товары"]
)


@router.get(
    "",
    response_model=ItemsResponse,
)
async def get_items(
    subcategory: str | None = Query(
        default=None,
        description="Категория товаров"
    ),
    item_service: ItemService = Depends(get_item_service),
):
    response = await item_service.get_items(subcategory)
    return response
