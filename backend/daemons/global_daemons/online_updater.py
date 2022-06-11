import asyncio
import time
import traceback

import aio_pika
from aio_pika import RobustChannel, RobustExchange, RobustQueue
from aioredis import Redis

from common.current_online import set_current_online
from common.redis import get_redis_cursor
from rabbitmq.globals import RabbitMQGlobals
from rabbitmq.modules import get_rabbitmq_connection, get_rabbitmq_channel, \
    declare_broadcast_exchange, declare_global_daemons_exchange
from web_sockets.schemas import WorkerOnlineReport, WSOutcomeMessageType, \
    WSOutcomeMessage


class OnlineUpdater:
    """Listens reports from app containers about their current online
    (calculated by counting connected websockets)
    and refreshes summary current online.

    """

    def __init__(self):
        self._authorized: dict[str, list[int]] = {}  # worker_id: [user_ids]
        self._unauthorized: dict[str, list[str]] = {}  # worker_id: [ips]
        self._last_activity: dict[str, int] = {}  # worker_id: timestamp of last report

        self._channel: RobustChannel | None = None
        self._broadcast_exchange: RobustExchange | None = None
        self._global_daemons_exchange: RobustExchange | None = None
        self._queue: RobustQueue | None = None

        self._redis_cursor: Redis | None = None

    async def run(self):
        await self._connect_dependencies()

        while True:
            try:
                await self._handle_messages()
            except:
                traceback.print_exc()
                await asyncio.sleep(3)

    def get_current_online(self) -> int:
        authorized = set(sum(self._authorized.values(), []))
        unauthorized = set(sum(self._unauthorized.values(), []))
        return len(authorized) + len(unauthorized)

    async def _connect_dependencies(self) -> None:
        connection = await get_rabbitmq_connection()

        self._channel = await get_rabbitmq_channel(connection)
        self._broadcast_exchange = await declare_broadcast_exchange(self._channel)
        self._global_daemons_exchange = await declare_global_daemons_exchange(self._channel)

        self._queue = await self._channel.declare_queue(
            RabbitMQGlobals.ONLINE_UPDATER_ROUTING_KEY,
            durable=True
        )
        await self._queue.bind(
            self._global_daemons_exchange,
            routing_key=RabbitMQGlobals.ONLINE_UPDATER_ROUTING_KEY
        )

        self._redis_cursor = await anext(get_redis_cursor())

    async def _handle_messages(self) -> None:
        last_update = time.time()
        last_online = -1

        async for message_ in self._queue:
            message = WorkerOnlineReport.parse_raw(message_.body.decode())
            self._authorized[message.worker_id] = message.authorized
            self._unauthorized[message.worker_id] = message.unauthorized
            self._last_activity[message.worker_id] = int(time.time())

            if time.time() - last_update >= 3:
                last_update = time.time()
                new_online = self.get_current_online()
                if new_online != last_online:
                    last_online = new_online
                    await self._broadcast_new_online(new_online)
                    await set_current_online(self._redis_cursor, new_online)

                self._clean_deprecated_data()

            await message_.ack()  # type: ignore

    async def _broadcast_new_online(self, new_online: int) -> None:
        message = WSOutcomeMessage(
            type=WSOutcomeMessageType.ONLINE_UPDATE,
            data={'new_online': new_online}
        )
        await self._broadcast_exchange.publish(
            aio_pika.Message(message.json().encode()),
            routing_key=''
        )

    def _clean_deprecated_data(self) -> None:
        for worker_id, last_message in list(self._last_activity.items()):
            if time.time() - last_message >= 10:
                del self._authorized[worker_id]
                del self._unauthorized[worker_id]
                del self._last_activity[worker_id]
