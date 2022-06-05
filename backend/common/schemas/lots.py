from datetime import datetime

from pydantic import BaseModel, Field

from .bids import BidInfo
from .items import ItemInfo


class LotCreateForm(BaseModel):
    item_id: int
    lifetime_in_minutes: int = Field(..., ge=1)


class LotCreate(LotCreateForm):
    owner_id: int


class LotUpdateForm(BaseModel):
    pass


class LotUpdate(BaseModel):
    is_canceled: bool | None = None
    win_bid_id: bool | None = None


class LotInfo(BaseModel):
    id: int
    owner_id: int
    item: ItemInfo | None
    is_canceled: bool
    max_bid: int
    created_at: datetime
    end_time: datetime

    class Config:
        orm_mode = True


class LotInfoExtended(LotInfo):
    win_bid: BidInfo | None
