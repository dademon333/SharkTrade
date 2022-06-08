import sqlalchemy.exc
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from common import crud
from common.db import get_db, UserStatus
from common.responses import UnauthorizedResponse, NotEnoughRightsResponse
from common.schemas.bids import BidInfoExtended, BidCreateForm, BidCreate
from common.security.auth import get_user_id, get_user_status
from lots.modules import raise_if_lot_not_exists, raise_if_lot_is_canceled
from lots.schemas import LotNotFoundResponse, LotIsCanceledResponse
from users.modules import raise_not_enough_money
from users.schemas import NotEnoughMoneyResponse, NewBalanceResponse, CantBidOnOwnLotResponse
from .modules import raise_if_exists_bigger_bid, raise_if_bid_not_exists, raise_if_no_access_to_edit_bid, raise_if_cant_withdraw_bid, raise_bid_already_withdrawn, raise_if_bidder_equals_lot_owner
from .schemas import BidsListResponse, ExistsBiggerBidResponse, BidNotFoundResponse, CantWithdrawBidResponse, BidAlreadyWithdrawnResponse

bids_router = APIRouter()


@bids_router.get(
    '/my',
    response_model=BidsListResponse,
    responses={401: {'model': UnauthorizedResponse}}
)
async def get_own_bids(
        limit: int = Query(25, ge=1, le=1000),
        before_id: int | None = Query(None, ge=0),
        user_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Возвращает ставки текущего пользователя в антихронологическом порядке."""
    bids = await crud.bids.get_by_owner_id(db, user_id, limit, before_id)
    amount = await crud.bids.get_user_bids_count(db, user_id)
    return BidsListResponse(
        total_amount=amount,
        bids=[BidInfoExtended.from_orm(x) for x in bids]
    )


@bids_router.post(
    '/',
    response_model=BidInfoExtended,
    responses={
        400: {
            'model':
                LotIsCanceledResponse
                | ExistsBiggerBidResponse
                | NotEnoughMoneyResponse
                | CantBidOnOwnLotResponse
        },
        401: {'model': UnauthorizedResponse},
        404: {'model': LotNotFoundResponse}
    }
)
async def create_bid(
        create_form: BidCreateForm,
        user_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Создает ставку."""
    lot_id = create_form.lot_id
    amount = create_form.amount

    lot = await crud.lots.get_by_id(db, lot_id)
    raise_if_lot_not_exists(lot)
    raise_if_lot_is_canceled(lot)
    raise_if_exists_bigger_bid(lot, amount)
    raise_if_bidder_equals_lot_owner(lot, user_id)

    try:
        await crud.users.decrement_balance(db, user_id, amount)
    except sqlalchemy.exc.IntegrityError:
        raise_not_enough_money()

    bid = await crud.bids.create(
        db, BidCreate(**create_form.dict(), owner_id=user_id)
    )
    return BidInfoExtended.from_orm(bid)


@bids_router.post(
    '/withdraw/{bid_id}',
    response_model=NewBalanceResponse,
    responses={
        400: {'model': CantWithdrawBidResponse | BidAlreadyWithdrawnResponse},
        401: {'model': UnauthorizedResponse},
        403: {'model': NotEnoughRightsResponse},
        404: {'model': BidNotFoundResponse}
    }
)
async def withdraw_bid(
        bid_id: int,
        user_id: int = Depends(get_user_id),
        user_status: UserStatus = Depends(get_user_status),
        db: AsyncSession = Depends(get_db)
):
    """Возвращает деньги с проигравшей ставки на баланс."""
    bid = await crud.bids.get_by_id(db, bid_id)
    raise_if_bid_not_exists(bid)
    raise_if_no_access_to_edit_bid(bid, user_id, user_status)
    raise_if_cant_withdraw_bid(bid)

    try:
        await crud.bids.set_is_withdrawn(db, bid.id)
    except AssertionError:
        raise_bid_already_withdrawn()

    await crud.users.increment_balance(db, user_id, bid.amount)
    user = await crud.users.get_by_id(db, user_id)
    return NewBalanceResponse(new_balance=user.rubles_balance)
