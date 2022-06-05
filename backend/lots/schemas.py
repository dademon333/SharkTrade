from pydantic import BaseModel

from common.schemas.lots import LotInfo, LotInfoExtended


class LotsListResponse(BaseModel):
    total_amount: int
    lots: list[LotInfo | LotInfoExtended]


class LotNotFoundResponse(BaseModel):
    detail: str = 'Lot not found'


class LotIsCanceledResponse(BaseModel):
    detail: str = 'Lot is canceled'
