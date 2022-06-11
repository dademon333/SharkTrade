import asyncio
import traceback

import aio_pika

from rabbitmq.globals import RabbitMQGlobals
from rabbitmq.modules import get_rabbitmq_channel, declare_global_daemons_exchange, \
    get_rabbitmq_connection
from web_sockets.manager import WebsocketsManager


async def online_updater():
    """Send report about local websockets connections to online updater once a second."""
    connection = await get_rabbitmq_connection()
    channel = await get_rabbitmq_channel(connection)
    exchange = await declare_global_daemons_exchange(channel)

    while True:
        try:
            connections = WebsocketsManager.get_current_connections()
            await exchange.publish(
                aio_pika.Message(connections.json().encode()),
                routing_key=RabbitMQGlobals.ONLINE_UPDATER_ROUTING_KEY
            )
            await asyncio.sleep(1)
        except:
            traceback.print_exc()
            await asyncio.sleep(1)
