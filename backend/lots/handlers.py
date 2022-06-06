from typing import Union

from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common import crud
from common.db import get_db, UserStatus
from common.responses import UnauthorizedResponse, NotEnoughRightsResponse, OkResponse
from common.schemas.lots import LotInfo, LotInfoExtended, LotCreateForm, \
    LotCreate, LotUpdate
from common.security.auth import get_user_id, get_user_id_soft, \
    get_user_status
from items.modules import raise_if_item_not_exists, \
    raise_if_no_access_to_edit_item, raise_item_is_locked
from items.schemas import ItemNotFoundResponse, ItemIsLockedResponse
from .modules import raise_if_lot_not_exists, raise_if_no_access_to_edit_lot, \
    raise_if_lot_is_canceled
from .schemas import LotsListResponse, LotNotFoundResponse, LotIsCanceledResponse

lots_router = APIRouter()


@lots_router.get(
    '/list',
    response_model=LotsListResponse
)
async def get_active_lots(
        limit: int = Query(25, ge=1, le=1000),
        offset: int = Query(0, ge=0),
        db: AsyncSession = Depends(get_db)
):
    """Возвращает активные лоты."""
    lots = await crud.lots.get_active(db, limit, offset)
    active_count = await crud.lots.get_active_count(db)
    return LotsListResponse(
        total_count=active_count,
        lots=[LotInfo.from_orm(x) for x in lots]
    )


@lots_router.get(
    '/my',
    response_model=LotsListResponse,
    responses={401: {'model': UnauthorizedResponse}}
)
async def get_own_lots(
        limit: int = Query(25, ge=1, le=1000),
        offset: int = Query(0, ge=0),
        user_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Возвращает лоты текущего пользователя."""
    lots = await crud.lots.get_by_owner_id(db, user_id, limit, offset)
    active_count = await crud.lots.get_active_count(db)
    return LotsListResponse(
        total_count=active_count,
        lots=[LotInfoExtended.from_orm(x) for x in lots]
    )


@lots_router.get(
    '/{lot_id}',
    response_model=Union[LotInfo, LotInfoExtended],
    responses={404: {'model': LotNotFoundResponse}}
)
async def get_lot(
        lot_id: int,
        user_id: int = Depends(get_user_id_soft),
        db: AsyncSession = Depends(get_db)
):
    """Возвращает информацию о лоте по идентификатору."""
    lot = await crud.lots.get_by_id(db, lot_id)
    raise_if_lot_not_exists(lot)

    if user_id != lot.owner_id:
        return LotInfo.from_orm(lot)
    else:
        return LotInfoExtended.from_orm(lot)


@lots_router.post(
    '/',
    response_model=LotInfoExtended,
    responses={
        400: {'model': ItemIsLockedResponse},
        401: {'model': UnauthorizedResponse},
        403: {'model': NotEnoughRightsResponse},
        404: {'model': ItemNotFoundResponse}
    }
)
async def create_lot(
        create_form: LotCreateForm,
        user_id: int = Depends(get_user_id),
        user_status: UserStatus = Depends(get_user_status),
        db: AsyncSession = Depends(get_db)
):
    """Создает лот."""
    item = await crud.items.get_by_id(db, create_form.item_id)
    raise_if_item_not_exists(item)
    raise_if_no_access_to_edit_item(item, user_id, user_status)

    try:
        lot = await crud.lots.create(
            db,
            LotCreate(**create_form.dict(), owner_id=item.owner_id)
        )
    except AssertionError:
        raise_item_is_locked()
        return

    return LotInfoExtended.from_orm(lot)


@lots_router.delete(
    '/{lot_id}',
    response_model=OkResponse,
    responses={
        400: {'model': LotIsCanceledResponse},
        401: {'model': UnauthorizedResponse},
        403: {'model': NotEnoughRightsResponse},
        404: {'model': LotNotFoundResponse}
    }
)
async def remove_lot(
        lot_id: int,
        user_id: int = Depends(get_user_id),
        user_status: UserStatus = Depends(get_user_status),
        db: AsyncSession = Depends(get_db)
):
    """Удаляет лот."""
    lot = await crud.lots.get_by_id(db, lot_id)
    raise_if_lot_not_exists(lot)
    raise_if_no_access_to_edit_lot(lot, user_id, user_status)
    raise_if_lot_is_canceled(lot)

    await crud.lots.update(db, lot.id, LotUpdate(is_canceled=True))
    await crud.items.unlock(db, lot.item_id)

    return OkResponse()
