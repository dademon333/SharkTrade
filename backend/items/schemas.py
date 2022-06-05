from pydantic import BaseModel

from common.schemas.items import ItemInfoExtended


class ItemsListResponse(BaseModel):
    total_count: int
    items: list[ItemInfoExtended]


class ItemNotFoundResponse(BaseModel):
    detail: str = 'Item not found'


class ItemIsLockedResponse(BaseModel):
    detail: str = 'Item is locked'
