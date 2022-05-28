from datetime import datetime

from pydantic import BaseModel
from pydantic.utils import GetterDict

from common.db import ProfilePhoto
from config import Config


class ProfilePhotoCreate(BaseModel):
    owner_id: int
    media_id: int


class ProfilePhotoUpdate(BaseModel):
    pass


class ProfilePhotoInfo(BaseModel):
    id: int
    owner_id: int
    url: str
    created_at: datetime

    class Config:
        orm_mode = True

        @classmethod
        def getter_dict(cls, profile_photo: {ProfilePhoto}):
            return {
                **GetterDict(profile_photo),
                'url': f'{Config.SERVER_URL}/media/{profile_photo.media_uuid}.png'
            }
