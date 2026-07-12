from datetime import date

from fastapi import APIRouter, Depends, Path, Query

from apps.item.schemas import ItemResponse, ItemRowsResponse, ItemsResponse
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
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Items per page",
    ),
    item_service: ItemService = Depends(get_item_service),
):
    response = await item_service.get_items(
        subcategory=subcategory,
        page=page,
        page_size=page_size,
    )
    return response


@router.get(
    "/{sku}",
    response_model=ItemResponse,
)
async def get_item(
    sku: str = Path(),
    item_service: ItemService = Depends(get_item_service),
):
    response = await item_service.get_item(sku)
    return response


@router.get(
    "/{sku}/rows",
    response_model=ItemRowsResponse,
)
async def get_item_rows(
    sku: str = Path(),
    date_from: date = Query(description="Дата начала"),
    date_to: date = Query(description="Дата окончания"),
    item_service: ItemService = Depends(get_item_service),
):
    response = await item_service.get_item_rows(
        sku=sku,
        date_from=date_from,
        date_to=date_to,
    )
    return response
