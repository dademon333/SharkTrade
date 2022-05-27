import socket

from fastapi import APIRouter, Depends

from common.db import UserStatus
from common.responses import UnauthorizedResponse, AdminStatusRequiredResponse
from common.security.auth import UserStatusChecker
from .schemas import HostnameResponse

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
