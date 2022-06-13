import uuid

from aio_pika import RobustConnection, RobustExchange, RobustQueue


class RabbitMQGlobals:
    # Read detailed description in web_sockets > README

    WS_BROADCAST_EXCHANGE_NAME = 'ws_broadcast'
    WS_DIRECT_MESSAGES_EXCHANGE_NAME = 'ws_direct_messages'
    GLOBAL_DAEMONS_EXCHANGE_NAME = 'global_daemons'

    # routing keys of global daemons
    ONLINE_UPDATER_ROUTING_KEY = 'online_updater'

    WORKER_ID = str(uuid.uuid4())

    # These fields fills by on_startup hook at backend_pre_start.py

    # Global RabbitMQ connection instance.
    CONNECTION: RobustConnection | None = None
    # Delivers direct messages for users between apps instances
    # which should be delivered to connected clients via websockets
    WS_DIRECT_MESSAGES_EXCHANGE: RobustExchange | None = None
    # The same, but for broadcasting messages
    WS_BROADCAST_EXCHANGE: RobustExchange | None = None
    # Listens described above messages to then send them
    # to users connected with this app instance.
    # Unique for each app instance.
    WS_QUEUE: RobustQueue | None = None

    # Send messages to global daemons here
    GLOBAL_DAEMONS_EXCHANGE: RobustExchange | None = None
