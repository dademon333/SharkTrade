import asyncio

import aio_pika
from fastapi import WebSocket
from starlette.websockets import WebSocketState

from rabbitmq.globals import RabbitMQGlobals
from .schemas import WSOutcomeMessage, WorkerOnlineReport


class WebsocketsManager:
    # Read detailed description in web_sockets > README

    # user_id: [websockets]
    _authorized_connections: dict[int, list[WebSocket]] = {}
    # ip: [websockets]
    _unauthorized_connections: dict[str, list[WebSocket]] = {}
    # websocket: ip | user_id
    _identifiers: dict[WebSocket, str | int] = {}

    @classmethod
    async def connect(
            cls,
            websocket: WebSocket,
            ip: str
    ) -> None:
        await websocket.accept()
        cls._identifiers[websocket] = ip

        if ip in cls._unauthorized_connections:
            cls._unauthorized_connections[ip].append(websocket)
        else:
            cls._unauthorized_connections[ip] = [websocket]

    @classmethod
    async def identify_connection(
            cls,
            websocket: WebSocket,
            user_id: int
    ) -> None:
        ip = cls._identifiers[websocket]
        cls._identifiers[websocket] = user_id
        cls._unauthorized_connections[ip].remove(websocket)

        if user_id in cls._authorized_connections:
            cls._authorized_connections[user_id].append(websocket)
        else:
            cls._authorized_connections[user_id] = [websocket]

    @classmethod
    async def disconnect(cls, websocket: WebSocket) -> None:
        identifier = cls._identifiers[websocket]
        del cls._identifiers[websocket]

        if isinstance(identifier, int):
            cls._authorized_connections[identifier].remove(websocket)
        else:
            cls._unauthorized_connections[identifier].remove(websocket)

        if websocket.application_state != WebSocketState.DISCONNECTED:
            try:
                await websocket.close()
            except:
                pass

    @classmethod
    async def send_message_to_websocket(
            cls,
            message: WSOutcomeMessage,
            websocket: WebSocket
    ):
        message = message.dict(exclude={'user_id'})
        await websocket.send_json(message)

    @classmethod
    async def send_direct_message(
            cls,
            message: WSOutcomeMessage
    ) -> None:
        await RabbitMQGlobals.WS_DIRECT_MESSAGES_EXCHANGE.publish(
            aio_pika.Message(message.json().encode()),
            routing_key=str(WSOutcomeMessage.user_id)
        )

    @classmethod
    async def send_direct_message_to_local_connections(
            cls,
            message: WSOutcomeMessage
    ) -> None:
        message = message.dict(exclude={'user_id'})
        user_connections = cls._authorized_connections.get(message['user_id'])

        if user_connections is not None:
            tasks = [socket.send_json(message) for socket in user_connections]
            await asyncio.gather(*tasks)

    @classmethod
    async def broadcast(cls, message: WSOutcomeMessage) -> None:
        await RabbitMQGlobals.WS_BROADCAST_EXCHANGE.publish(
            aio_pika.Message(message.json().encode()),
            routing_key=''
        )

    @classmethod
    async def broadcast_local_connection(
            cls,
            message: WSOutcomeMessage
    ) -> None:
        connections = list(cls._authorized_connections.values())
        connections += list(cls._unauthorized_connections.values())
        connections = sum(connections, [])  # Zip 2D array to 1D

        message = message.dict(exclude={'user_id'})
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
