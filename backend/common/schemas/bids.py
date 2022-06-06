from datetime import datetime

from pydantic import BaseModel
from pydantic.utils import GetterDict

from common.db import Bid


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

    class Config:
        orm_mode = True


class BidInfoExtended(BidInfo):
    is_withdrawn: bool
    can_withdraw: bool
    created_at: datetime

    @classmethod
    def getter_dict(cls, bid: Bid):
        from bids.modules import can_withdraw_bid
        return {
            **GetterDict(bid),
            'can_withdraw': can_withdraw_bid(bid)
        }
