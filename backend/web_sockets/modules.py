import json

from aioredis import Redis
from starlette.websockets import WebSocket

from common.security.auth import get_user_id_soft
from .manager import WebsocketsManager
from .schemas import WSIncomeMessageType, WSOutcomeMessage, \
    WSOutcomeMessageType


async def handle_message(
        message: str,
        websocket: WebSocket,
        redis_cursor: Redis
) -> None:
    try:
        message = json.loads(message)
    except:
        return

    match message.get('type'):
        case WSIncomeMessageType.AUTH:
            await _on_auth(message, websocket, redis_cursor)
        case _:
            pass


async def _on_auth(
        message: dict,
        websocket: WebSocket,
        redis_cursor: Redis
) -> None:
    access_token = message.get('access_token', '')
    user_id = await get_user_id_soft(redis_cursor, access_token)
    if user_id is not None:
        await WebsocketsManager.identify_connection(websocket, user_id)

    message = WSOutcomeMessage(
        type=WSOutcomeMessageType.AUTH_RESULT,
        data={'success': user_id is not None}
    )
    await WebsocketsManager.send_message_to_websocket(message, websocket)
