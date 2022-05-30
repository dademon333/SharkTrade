from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from common import crud
from common.db import get_db
from common.redis import get_redis_cursor
from common.responses import OkResponse, UnauthorizedResponse
from common.security.auth import check_auth, oauth2_scheme
from common.security.users import hash_password
from .schemas import LoginErrorResponse, AccessTokenResponse

auth_router = APIRouter()


@auth_router.post(
    '/login',
    response_model=AccessTokenResponse,
    responses={403: {'model': LoginErrorResponse}}
)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db),
        redis_cursor: Redis = Depends(get_redis_cursor)
):
    """Адрес этого endpoint'а дает исчерпывающую информацию о его предназначении.

    Если все окей, возвращает access_token.
    Срок жизни токена - 30 дней.

    """
    user = await crud.users.get_by_nickname_or_email(db, form_data.username)
    if user is None \
            or hash_password(user.id, form_data.password) != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=LoginErrorResponse().detail
        )

    access_token = await crud.user_tokens.create(user.id, redis_cursor)
    return {'access_token': access_token, 'token_type': 'bearer'}


@auth_router.delete(
    '/logout',
    response_model=OkResponse,
    responses={401: {'model': UnauthorizedResponse}},
    dependencies=[Depends(check_auth)]
)
async def logout(
        redis_cursor: Redis = Depends(get_redis_cursor),
        access_token: str = Depends(oauth2_scheme)
):
    """Адрес этого endpoint'а дает исчерпывающую информацию о его предназначении.

    Удаляет информацию о токене на сервере.

    """
    await crud.user_tokens.delete(access_token, redis_cursor)
    return OkResponse()
