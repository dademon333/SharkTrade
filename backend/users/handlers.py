import sqlalchemy.exc
from aioredis import Redis
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import AccessTokenResponse
from common import crud
from common.redis import get_redis_cursor
from common.responses import OkResponse, UnauthorizedResponse, \
    AdminStatusRequiredResponse
from common.security.auth import get_user_id, UserStatusChecker
from common.db import get_db, UserStatus
from common.schemas.users import UserCreateForm, UserUpdateForm, UserInfo, \
    UserInfoExtended
from .modules import raise_if_user_not_exist, handle_user_constraint_conflict
from .schemas import UserNotFoundResponse, EmailAlreadyExistsResponse, \
    UsernameAlreadyExistsResponse

users_router = APIRouter()


@users_router.get(
    '/list',
    response_model=list[UserInfoExtended],
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def list_users(
        limit: int = Query(250, le=1000),
        offset: int = 0,
        db: AsyncSession = Depends(get_db)
):
    """Возвращает информацию о всех пользователях. Требует статус admin."""
    users = await crud.users.get_many(db, limit, offset)
    return [UserInfoExtended.from_orm(x) for x in users]


@users_router.get(
    '/me',
    response_model=UserInfoExtended,
    responses={401: {'model': UnauthorizedResponse}}
)
async def get_self_info(
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_user_id)
):
    """Возвращает информацию о текущем пользователе."""
    user = await crud.users.get_by_id(db, user_id)
    return UserInfoExtended.from_orm(user)


@users_router.get(
    '/{user_id}',
    response_model=UserInfo,
    responses={404: {'model': UserNotFoundResponse}}
)
async def get_user_info(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Возвращает информацию о пользователе по его id. Требует статус admin."""
    user = await crud.users.get_by_id(db, user_id)
    raise_if_user_not_exist(user)
    return UserInfo.from_orm(user)


@users_router.post(
    '/',
    response_model=AccessTokenResponse,
    responses={
        409: {'model': UsernameAlreadyExistsResponse | EmailAlreadyExistsResponse}
    }
)
async def create_user(
        create_form: UserCreateForm,
        db: AsyncSession = Depends(get_db),
        redis_cursor: Redis = Depends(get_redis_cursor)
):
    """Создает нового пользователя."""
    try:
        user = await crud.users.create(db, create_form)
    except sqlalchemy.exc.IntegrityError as exc:
        handle_user_constraint_conflict(exc)
        return

    access_token = await crud.user_tokens.create(user.id, redis_cursor)
    return {'access_token': access_token, 'token_type': 'bearer'}


@users_router.put(
    '/me',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        409: {'model': UsernameAlreadyExistsResponse | EmailAlreadyExistsResponse}
    }
)
async def update_self(
        update_form: UserUpdateForm,
        user_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Обновляет данные о текущем пользователе."""
    try:
        await crud.users.update(db, user_id, update_form)
    except sqlalchemy.exc.IntegrityError as exc:
        handle_user_constraint_conflict(exc)
    return OkResponse()


@users_router.put(
    '/{user_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        404: {'model': UserNotFoundResponse},
        409: {'model': EmailAlreadyExistsResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def update_user(
        user_id: int,
        update_form: UserUpdateForm,
        db: AsyncSession = Depends(get_db)
):
    """Обновляет данные о пользователе. Требует статус admin."""
    user = await crud.users.get_by_id(db, user_id)
    raise_if_user_not_exist(user)

    try:
        await crud.users.update(db, user_id, update_form)
    except sqlalchemy.exc.IntegrityError as exc:
        handle_user_constraint_conflict(exc)
    return OkResponse()


@users_router.delete(
    '/{user_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
        404: {'model': UserNotFoundResponse}
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Удаляет пользователя. Требует статус admin."""
    user = await crud.users.get_by_id(db, user_id)
    raise_if_user_not_exist(user)
    await crud.users.delete(db, user_id)
    return OkResponse()
