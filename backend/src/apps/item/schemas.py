from datetime import date

from pydantic import BaseModel, ConfigDict

from apps.item.enums import BiasDirection


class ItemResponse(BaseModel):
    sku: str
    name: str
    subcategory: str


class ItemsResponse(BaseModel):
    items: list[ItemResponse]
    has_next: bool


class ItemRowResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    date: date
    fact: float | None
    sales: float | None
    math: float
    ml: float
    ruki: float | None


class ItemMetrics(BaseModel):
    fa: float
    bias: float
    bias_direction: BiasDirection


class ItemRowsResponse(BaseModel):
    rows: list[ItemRowResponse]
    metrics: ItemMetrics
