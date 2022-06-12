from datetime import datetime

from pydantic import BaseModel, validator

from .bids import BidInfo
from .items import ItemInfo
from ..responses import END_TIME_MUST_BE_GREATER_NOW


class LotCreateForm(BaseModel):
    item_id: int
    end_time: datetime

    @validator('end_time')
    def end_time_greater_now(cls, value: datetime) -> datetime:
        if value <= datetime.now():
            raise ValueError(END_TIME_MUST_BE_GREATER_NOW)
        return value


class LotCreate(LotCreateForm):
    owner_id: int


class LotUpdateForm(BaseModel):
    pass


class LotUpdate(BaseModel):
    is_cancelled: bool | None = None
    win_bid_id: int | None = None


class LotInfo(BaseModel):
    id: int
    owner_id: int
    item: ItemInfo | None
    is_cancelled: bool
    max_bid: int
    created_at: datetime
    end_time: datetime

    class Config:
        orm_mode = True


class LotInfoExtended(LotInfo):
    bids: list[BidInfo]
