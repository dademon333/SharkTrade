from datetime import datetime

from pydantic import BaseModel
from pydantic.utils import GetterDict

from config import Config
from ..db import ItemPhoto


class ItemPhotoCreateForm(BaseModel):
    item_id: int
    media_uuid: str


class ItemPhotoCreate(BaseModel):
    item_id: int
    media_id: int


class ItemPhotoUpdateForm(BaseModel):
    pass


class ItemPhotoUpdate(BaseModel):
    pass


class ItemPhotoInfo(BaseModel):
    id: int
    item_id: int
    url: str
    created_at: datetime

    class Config:
        orm_mode = True

        @classmethod
        def getter_dict(cls, item_photo: ItemPhoto):
            return {
                **GetterDict(item_photo),
                'url': f'{Config.SERVER_URL}/media/{item_photo.media_uuid}.png'
            }
