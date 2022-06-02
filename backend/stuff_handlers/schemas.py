from pydantic import BaseModel


class HostnameResponse(BaseModel):
    hostname: str


class CurrentOnlineResponse(BaseModel):
    current_online: int
