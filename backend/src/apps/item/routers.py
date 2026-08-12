from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from apps.item.exceptions import ItemNotFoundError
from apps.item.schemas import ItemResponse, ItemRowsQuery, ItemRowsResponse, ItemsResponse
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
    subcategory: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=100,
            pattern=r"^\S(?:.*\S)?$",
            description="Категория товаров",
        ),
    ] = None,
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
    sku: Annotated[str, Path(
        min_length=11,
        max_length=11,
        pattern=r"^\d{2}-\d{8}$",
        description="SKU в формате NN-NNNNNNNN",
    )],
    item_service: ItemService = Depends(get_item_service),
):
    try:
        response = await item_service.get_item(sku)
    except ItemNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return response


@router.get(
    "/{sku}/rows",
    response_model=ItemRowsResponse,
)
async def get_item_rows(
    sku: Annotated[str, Path(
        min_length=11,
        max_length=11,
        pattern=r"^\d{2}-\d{8}$",
        description="SKU в формате NN-NNNNNNNN",
    )],
    query: Annotated[ItemRowsQuery, Query()],
    item_service: ItemService = Depends(get_item_service),
):
    try:
        response = await item_service.get_item_rows(
            sku=sku,
            date_from=query.date_from,
            date_to=query.date_to,
        )
    except ItemNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return response
