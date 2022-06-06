import socket

from aioredis import Redis
from fastapi import APIRouter, Depends

from common.current_online import get_current_online
from common.db import UserStatus
from common.redis import get_redis_cursor
from common.responses import UnauthorizedResponse, AdminStatusRequiredResponse
from common.security.auth import UserStatusChecker
from .schemas import HostnameResponse, CurrentOnlineResponse

stuff_router = APIRouter()


@stuff_router.get(
    '/hostname',
    response_model=HostnameResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': AdminStatusRequiredResponse},
    },
    dependencies=[Depends(UserStatusChecker(min_status=UserStatus.ADMIN))]
)
async def get_hostname():
    """Возвращает hostname сервера(контейнера), в котором запущен код.

    Можно использовать для проверки работы вертикального масштабирования,
    хотя в основном используется для тестов во время разработки.

    """
    return HostnameResponse(hostname=socket.gethostname())


@stuff_router.get(
    '/current_online',
    response_model=CurrentOnlineResponse
)
async def _get_current_online(
        redis_cursor: Redis = Depends(get_redis_cursor),
):
    """Возвращает текущий онлайн."""
    current_online = await get_current_online(redis_cursor)
    return CurrentOnlineResponse(current_online=current_online)
