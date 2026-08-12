from datetime import date

from pydantic import BaseModel, ConfigDict, model_validator

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


class ItemRowsQuery(BaseModel):
    date_from: date
    date_to: date

    @model_validator(mode="after")
    def validate_date_range(self) -> "ItemRowsQuery":
        if self.date_from > self.date_to:
            raise ValueError("date_from must be before or equal to date_to")

        return self
