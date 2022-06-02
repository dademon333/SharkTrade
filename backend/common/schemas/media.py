from datetime import datetime

from pydantic import BaseModel


class MediaCreate(BaseModel):
    uuid: str
    owner_id: int


class MediaUpdate(BaseModel):
    pass


class MediaInfo(BaseModel):
    id: int
    uuid: str
    owner_id: int
    created_at: datetime
