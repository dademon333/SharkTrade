import aio_pika
from aio_pika import RobustConnection, RobustChannel, RobustExchange, ExchangeType, RobustQueue

from tokens import Tokens
from .globals import RabbitMQGlobals


async def get_rabbitmq_connection() -> RobustConnection:
    return await aio_pika.connect_robust(    # type: ignore
        host=Tokens.RABBITMQ_HOST,
        login=Tokens.RABBITMQ_USERNAME,
        password=Tokens.RABBITMQ_PASSWORD
    )


async def get_rabbitmq_channel(connection: RobustConnection | None = None) -> RobustChannel:
    if connection is None:
        connection = RabbitMQGlobals.CONNECTION

    return await connection.channel()  # type: ignore


async def declare_direct_messages_exchange(channel: RobustChannel) -> RobustExchange:
    return await channel.declare_exchange(  # type: ignore
        RabbitMQGlobals.WS_DIRECT_MESSAGES_EXCHANGE_NAME,
        durable=True,
    )


async def declare_broadcast_exchange(channel: RobustChannel) -> RobustExchange:
    return await channel.declare_exchange(  # type: ignore
        RabbitMQGlobals.WS_BROADCAST_EXCHANGE_NAME,
        durable=True,
        type=ExchangeType.FANOUT
    )


async def declare_global_daemons_exchange(channel: RobustChannel) -> RobustExchange:
    return await channel.declare_exchange(  # type: ignore
        RabbitMQGlobals.GLOBAL_DAEMONS_EXCHANGE_NAME,
        durable=True
    )


async def declare_ws_message_queue(channel: RobustChannel) -> RobustQueue:
    return await channel.declare_queue(  # type: ignore
        f'ws_messages_{RabbitMQGlobals.WORKER_ID}',
        auto_delete=True
    )
