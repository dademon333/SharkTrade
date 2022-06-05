from datetime import datetime

from pydantic import BaseModel


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
