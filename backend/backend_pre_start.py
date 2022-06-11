import asyncio
import threading

from aio_pika import RobustChannel

from daemons.local_daemons.online_updater import online_updater
from daemons.local_daemons.websockets_synchronizer import websockets_synchronizer
from rabbitmq.globals import RabbitMQGlobals
from rabbitmq.modules import get_rabbitmq_connection, \
    declare_direct_messages_exchange, declare_broadcast_exchange, \
    declare_global_daemons_exchange, declare_ws_message_queue


async def on_startup():
    """FastAPI on_startup hook"""
    await _connect_rabbitmq()

    # Running local daemon workers.
    # You can find their common description at daemons -> local -> README.
    threading.Thread(target=asyncio.run, args=(online_updater(),), daemon=True).start()
    threading.Thread(target=asyncio.run, args=(websockets_synchronizer(),), daemon=True).start()



async def _connect_rabbitmq():
    connection = await get_rabbitmq_connection()
    channel: RobustChannel = await connection.channel()  # type: ignore

    broadcast_exchange = await declare_broadcast_exchange(channel)
    queue = await declare_ws_message_queue(channel)
    await queue.bind(broadcast_exchange)

    RabbitMQGlobals.CONNECTION = connection
    RabbitMQGlobals.WS_DIRECT_MESSAGES_EXCHANGE = await declare_direct_messages_exchange(channel)
    RabbitMQGlobals.WS_BROADCAST_EXCHANGE_NAME = broadcast_exchange
    RabbitMQGlobals.WS_QUEUE = queue

    RabbitMQGlobals.GLOBAL_DAEMONS_EXCHANGE = await declare_global_daemons_exchange(channel)
