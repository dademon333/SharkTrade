import asyncio
import json

from rabbitmq.modules import get_rabbitmq_connection, get_rabbitmq_channel, declare_ws_message_queue
from web_sockets.manager import WebsocketsManager
from web_sockets.schemas import WSDirectMessage, WSBroadcastMessage


async def websockets_synchronizer():
    connection = await get_rabbitmq_connection()
    channel = await get_rabbitmq_channel(connection)
    queue = await declare_ws_message_queue(channel)

    async for message_ in queue:
        message = json.loads(message_.body.decode())  # type: ignore
        if message['message_type'] == 'direct':
            message = WSDirectMessage.parse_obj(message)
            asyncio.create_task(
                WebsocketsManager.send_direct_message_to_local_connections(message)
            )
        else:
            message = WSBroadcastMessage.parse_obj(message)
            asyncio.create_task(
                WebsocketsManager.broadcast_local_connection(message)
            )

        await message_.ack()  # type: ignore
