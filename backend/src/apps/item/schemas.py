from pydantic import BaseModel


class ItemResponse(BaseModel):
    sku: str
    name: str
    subcategory: str


class ItemsResponse(BaseModel):
    items: list[ItemResponse]
