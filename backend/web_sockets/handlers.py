import traceback

from aioredis import Redis
from fastapi import APIRouter, Depends, Header
from starlette.websockets import WebSocket, WebSocketDisconnect

from common.redis import get_redis_cursor
from .manager import WebsocketsManager
from .modules import handle_message

websockets_router = APIRouter()


@websockets_router.websocket('/')
async def connect_websocket(
        websocket: WebSocket,
        ip: str = Header(..., alias='X-Real-IP'),
        redis_cursor: Redis = Depends(get_redis_cursor)
):
    await WebsocketsManager.connect(websocket, ip)

    try:
        while True:
            message = await websocket.receive_text()
            try:
                await handle_message(message, websocket, redis_cursor)
            except:
                traceback.print_exc()

    except WebSocketDisconnect:
        await WebsocketsManager.disconnect(websocket)
