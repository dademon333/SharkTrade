from pydantic import BaseModel

from common.schemas.bids import BidInfoExtended


class BidsListResponse(BaseModel):
    total_amount: int
    bids: list[BidInfoExtended]


class ExistsBiggerBidResponse(BaseModel):
    detail: str = 'Exists bigger bid'


class BidNotFoundResponse(BaseModel):
    detail: str = 'Bid not found'


class CantWithdrawBidResponse(BaseModel):
    detail: str = 'Can\'t withdraw bid'


class BidAlreadyWithdrawnResponse(BaseModel):
    detail: str = 'Bid already withdrawn'
