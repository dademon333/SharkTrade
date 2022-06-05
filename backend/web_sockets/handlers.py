import traceback

from aioredis import Redis
from fastapi import APIRouter, Depends, Header, Query, HTTPException
from starlette.websockets import WebSocket, WebSocketDisconnect

from common.redis import get_redis_cursor
from common.security.auth import get_user_id_soft
from web_sockets.manager import WebsocketsManager

websockets_router = APIRouter()


@websockets_router.websocket('/')
async def connect_websocket(
        websocket: WebSocket,
        access_token: str | None = Query(None),
        ip: str = Header(..., alias='X-Real-IP'),
        redis_cursor: Redis = Depends(get_redis_cursor)
):
    try:
        user_id = await get_user_id_soft(redis_cursor, access_token)
    except HTTPException:
        await websocket.close(3000)
        return
    except:
        traceback.print_exc()
        return

    if user_id is not None:
        await WebsocketsManager.connect_by_user_id(websocket, user_id)
    else:
        await WebsocketsManager.connect_by_ip(websocket, ip)

    try:
        while True:
            # noinspection PyUnusedLocal
            message = await websocket.receive_text()
            ...
    except WebSocketDisconnect:
        if user_id is not None:
            await WebsocketsManager.disconnect_by_user_id(websocket, user_id)
        else:
            await WebsocketsManager.disconnect_by_ip(websocket, ip)
