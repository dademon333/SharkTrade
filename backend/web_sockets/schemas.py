from enum import Enum
from typing import Any

from pydantic import BaseModel


class WSDirectMessageType(str, Enum):
    BALANCE_UPDATE = 'balance_update'


class WSBroadcastMessageType(str, Enum):
    ONLINE_UPDATE = 'online_update'


class WSDirectMessage(BaseModel):
    message_type = 'direct'
    type: WSDirectMessageType
    user_id: int
    data: dict[Any, Any]


class WSBroadcastMessage(BaseModel):
    message_type = 'broadcast'
    type: WSBroadcastMessageType
    data: dict[Any, Any]


class WorkerOnlineReport(BaseModel):
    worker_id: str
    authorized: list[int]
    unauthorized: list[str]
