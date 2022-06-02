import asyncio

import aio_pika
from fastapi import WebSocket
from starlette.websockets import WebSocketState

from rabbitmq.globals import RabbitMQGlobals
from .schemas import WSDirectMessage, WSBroadcastMessage, WorkerOnlineReport


class WebsocketsManager:
    # user_id: [connections]
    _authorized_connections: dict[int, list[WebSocket]] = {}
    # ip: [connections]
    _unauthorized_connections: dict[str, list[WebSocket]] = {}

    @classmethod
    async def connect_by_user_id(
            cls,
            websocket: WebSocket,
            user_id: int
    ) -> None:
        await websocket.accept()

        if user_id in cls._authorized_connections:
            cls._authorized_connections[user_id].append(websocket)
        else:
            await RabbitMQGlobals.WS_QUEUE.bind(
                RabbitMQGlobals.WS_DIRECT_MESSAGES_EXCHANGE,
                str(user_id)
            )
            cls._authorized_connections[user_id] = [websocket]

    @classmethod
    async def connect_by_ip(
            cls,
            websocket: WebSocket,
            ip: str
    ) -> None:
        await websocket.accept()

        if ip in cls._unauthorized_connections:
            cls._unauthorized_connections[ip].append(websocket)
        else:
            cls._unauthorized_connections[ip] = [websocket]

    @classmethod
    async def disconnect_by_user_id(
            cls,
            websocket: WebSocket,
            user_id: int
    ) -> None:
        if websocket in cls._authorized_connections[user_id]:
            cls._authorized_connections[user_id].remove(websocket)

        if websocket.application_state != WebSocketState.DISCONNECTED:
            try:
                await websocket.close()
            except:
                pass

    @classmethod
    async def disconnect_by_ip(
            cls,
            websocket: WebSocket,
            ip: str
    ) -> None:
        if websocket in cls._unauthorized_connections[ip]:
            cls._unauthorized_connections[ip].remove(websocket)

        if websocket.application_state != WebSocketState.DISCONNECTED:
            try:
                await websocket.close()
            except:
                pass

    @classmethod
    async def send_direct_message(
            cls,
            message: WSDirectMessage
    ) -> None:
        await RabbitMQGlobals.WS_DIRECT_MESSAGES_EXCHANGE.publish(
            aio_pika.Message(message.json().encode()),
            routing_key=str(WSDirectMessage.user_id)
        )

    @classmethod
    async def send_direct_message_to_local_connections(
            cls,
            message: WSDirectMessage
    ) -> None:
        message = message.dict()
        user_connections = cls._authorized_connections.get(message['user_id'])

        if user_connections is not None:
            tasks = [socket.send_json(message) for socket in user_connections]
            await asyncio.gather(*tasks)

    @classmethod
    async def broadcast(cls, message: WSBroadcastMessage) -> None:
        await RabbitMQGlobals.WS_BROADCAST_EXCHANGE.publish(
            aio_pika.Message(message.json().encode()),
            routing_key=''
        )

    @classmethod
    async def broadcast_local_connection(cls, message: WSBroadcastMessage) -> None:
        connections = list(cls._authorized_connections.values())
        connections += list(cls._unauthorized_connections.values())
        connections = sum(connections, [])  # Zip 2D array to 1D

        message = message.dict()
        tasks = [socket.send_json(message) for socket in connections]
        await asyncio.gather(*tasks)

    @classmethod
    def get_current_connections(cls) -> WorkerOnlineReport:
        authorized = [
            user_id
            for user_id, connections in cls._authorized_connections.items()
            if connections != []
        ]
        unauthorized = [
            ip
            for ip, connections in cls._unauthorized_connections.items()
            if connections != []
        ]
        return WorkerOnlineReport(
            worker_id=RabbitMQGlobals.WORKER_ID,
            authorized=authorized,
            unauthorized=unauthorized
        )
