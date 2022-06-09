from enum import Enum

from pydantic import BaseModel


class WSOutcomeMessageType(str, Enum):
    BALANCE_UPDATE = 'balance_update'
    ONLINE_UPDATE = 'online_update'
    AUTH_RESULT = 'auth_result'


class WSIncomeMessageType(str, Enum):
    AUTH = 'auth'


class WSOutcomeMessage(BaseModel):
    user_id: int | None = None
    type: WSOutcomeMessageType
    data: dict


class WorkerOnlineReport(BaseModel):
    worker_id: str
    authorized: list[int]
    unauthorized: list[str]
