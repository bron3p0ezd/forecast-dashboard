from datetime import date

from fastapi import HTTPException, status

from apps.item.enums import BiasDirection
from apps.item.models import Daily, Item
from apps.item.services import ItemService
from apps.item.repositories import DailyRepository, ItemRepository
from apps.item.schemas import ItemMetrics, ItemResponse, ItemRowResponse, ItemRowsResponse, ItemsResponse


class ItemServiceImpl(ItemService):
    def __init__(
        self,
        repository: ItemRepository,
        daily_repository: DailyRepository,
    ) -> None:
        self.__repository = repository
        self.__daily_repository = daily_repository

    async def get_items(
        self,
        subcategory: str | None,
        page: int,
        page_size: int,
    ) -> ItemsResponse:
        items = await self.__repository.select_items_by_subcategory(
            subcategory=subcategory,
            limit=page_size + 1,
            offset=(page - 1) * page_size,
        )

        return self.__build_items_response(
            items=items[:page_size],
            has_next=len(items) > page_size,
        )

    async def get_item(
        self,
        sku: str,
    ) -> ItemResponse | None:
        item = await self.__repository.select_item_by_sku(sku)

        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found",
            )

        return self.__build_item_response(item)

    async def get_item_rows(
        self,
        sku: str,
        date_from: date,
        date_to: date,
    ) -> ItemRowsResponse:
        rows = await self.__daily_repository.select_item_rows(
            sku=sku,
            date_from=date_from,
            date_to=date_to,
        )

        return self.__build_item_rows_response(rows)
        
    def __build_items_response(
        self,
        items: list[Item],
        has_next: bool,
    ) -> ItemsResponse:
        return ItemsResponse(
            items=[self.__build_item_response(item) for item in items],
            has_next=has_next,
        )

    def __build_item_response(
        self,
        item: Item,
    ) -> ItemResponse:
        return ItemResponse(
            sku=item.item_id,
            name=item.item_name,
            subcategory=item.subcategory,
        )

    def __build_item_rows_response(
        self,
        rows: list[Daily],
    ) -> ItemRowsResponse:
        return ItemRowsResponse(
            rows=[
                ItemRowResponse.model_validate(row)
                for row in rows
            ],
            metrics=self.__build_item_metrics(rows),
        )

    def __build_item_metrics(
        self,
        rows: list[Daily],
    ) -> ItemMetrics:
        fact_sum = 0.0
        absolute_error_sum = 0.0
        bias_sum = 0.0

        for row in rows:
            if row.fact is None:
                continue

            forecast = row.ruki if row.ruki is not None else row.ml
            fact_sum += row.fact
            absolute_error_sum += abs(forecast - row.fact)
            bias_sum += forecast - row.fact

        if fact_sum == 0:
            return ItemMetrics(
                fa=0,
                bias=0,
                bias_direction=BiasDirection.UP,
            )

        fa = max(0, 1 - absolute_error_sum / fact_sum) * 100
        bias = abs(bias_sum) / fact_sum * 100

        return ItemMetrics(
            fa=round(fa, 2),
            bias=round(bias, 2),
            bias_direction=(
                BiasDirection.UP
                if bias_sum >= 0
                else BiasDirection.DOWN
            ),
        )
