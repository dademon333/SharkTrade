from typing import Union

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from common import crud
from common.db import get_db, UserStatus
from common.responses import UnauthorizedResponse, OkResponse, \
    NotEnoughRightsResponse
from common.schemas.items import ItemInfo, ItemCreateForm, ItemCreate, \
    ItemUpdateForm, ItemInfoExtended
from common.security.auth import get_user_id, get_user_status, get_user_id_soft
from .modules import raise_if_item_not_exist, raise_if_no_access_to_edit_item
from .schemas import ItemsListResponse, ItemNotFoundResponse

items_router = APIRouter()


@items_router.get(
    '/my',
    response_model=ItemsListResponse,
    responses={401: {'model': UnauthorizedResponse}}
)
async def get_own_items(
        limit: int = Query(25, le=1000),
        offset: int = Query(0),
        user_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Возвращает предметы, принадлежащие пользователю."""
    items = await crud.items.get_by_owner_id(db, user_id, limit, offset)
    count = await crud.items.get_user_items_count(db, user_id)
    return ItemsListResponse(
        total_amount=count,
        items=[ItemInfoExtended.from_orm(x) for x in items]
    )


@items_router.get(
    '/{item_id}',
    response_model=Union[ItemInfo, ItemInfoExtended],
    responses={404: {'model': ItemNotFoundResponse}}
)
async def get_item(
        item_id: int,
        user_id: int = Depends(get_user_id_soft),
        db: AsyncSession = Depends(get_db)
):
    """Возвращает информацию о предмете по идентификатору."""
    item = await crud.items.get_by_id(db, item_id)
    raise_if_item_not_exist(item)

    if user_id != item.owner_id:
        return ItemInfo.from_orm(item)
    else:
        return ItemInfoExtended.from_orm(item)


@items_router.post(
    '/',
    response_model=ItemInfoExtended,
    responses={401: {'model': UnauthorizedResponse}}
)
async def create_item(
        item: ItemCreateForm,
        user_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Создает предмет."""
    item = await crud.items.create(
        db,
        ItemCreate(**item.dict(), owner_id=user_id)
    )
    return ItemInfoExtended.from_orm(item)


@items_router.put(
    '/{item_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': NotEnoughRightsResponse},
        404: {'model': ItemNotFoundResponse}
    }
)
async def update_item(
        item_id: int,
        update_form: ItemUpdateForm,
        user_id: int = Depends(get_user_id),
        user_status: UserStatus = Depends(get_user_status),
        db: AsyncSession = Depends(get_db)
):
    """Обновляет информацию о предмете."""
    item = await crud.items.get_by_id(db, item_id)
    raise_if_item_not_exist(item)
    raise_if_no_access_to_edit_item(item, user_id, user_status)
    await crud.items.update(db, item_id, update_form)
    return OkResponse()


@items_router.delete(
    '/{item_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': NotEnoughRightsResponse},
        404: {'model': ItemNotFoundResponse}
    }
)
async def delete_item(
        item_id: int,
        user_id: int = Depends(get_user_id),
        user_status: UserStatus = Depends(get_user_status),
        db: AsyncSession = Depends(get_db)
):
    """Удаляет предмет."""
    item = await crud.items.get_by_id(db, item_id)
    raise_if_item_not_exist(item)
    raise_if_no_access_to_edit_item(item, user_id, user_status)
    await crud.items.delete(db, item_id)
    return OkResponse()
