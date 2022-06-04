from pydantic import BaseModel

from common.schemas.items import ItemInfoExtended


class ItemsListResponse(BaseModel):
    total_amount: int
    items: list[ItemInfoExtended]


class ItemNotFoundResponse(BaseModel):
    detail: str = 'Item not found'
