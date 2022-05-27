from pydantic import BaseModel


class HostnameResponse(BaseModel):
    hostname: str
