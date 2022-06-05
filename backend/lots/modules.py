from fastapi import HTTPException, status

from common.db import Lot, UserStatus
from common.responses import NotEnoughRightsResponse
from .schemas import LotNotFoundResponse, LotIsCanceledResponse


def raise_if_lot_not_exist(lot: Lot):
    if lot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=LotNotFoundResponse().detail
        )


def raise_if_no_access_to_edit_lot(
        lot: Lot,
        user_id: int,
        user_status: UserStatus
) -> None:
    if lot.owner_id != user_id and user_status != UserStatus.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=NotEnoughRightsResponse().detail
        )


def raise_if_lot_is_canceled(lot: Lot) -> None:
    if lot.is_canceled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=LotIsCanceledResponse().detail
        )
