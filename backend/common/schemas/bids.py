from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from pydantic.utils import GetterDict

from .items import ItemInfo
from ..db import Bid


class BidStatus(str, Enum):
    WIN = 'win'
    HIGHEST = 'highest'
    LOSE = 'lose'


class BidCreateForm(BaseModel):
    lot_id: int
    amount: int


class BidCreate(BidCreateForm):
    owner_id: int


class BidUpdateForm(BaseModel):
    pass


class BidUpdate(BaseModel):
    pass


class BidInfo(BaseModel):
    id: int
    owner_id: int
    lot_id: int
    amount: int
    created_at: datetime

    class Config:
        orm_mode = True


class BidInfoExtended(BidInfo):
    is_withdrawn: bool
    can_withdraw: bool
    created_at: datetime

    status: BidStatus
    item: ItemInfo

    class Config:
        orm_mode = True

        @classmethod
        def getter_dict(cls, bid: Bid):
            from bids.modules import can_withdraw_bid, get_bid_status
            return {
                **GetterDict(bid),
                'item': ItemInfo.from_orm(bid.lot.item),
                'status': get_bid_status(bid),
                'can_withdraw': can_withdraw_bid(bid)
            }
