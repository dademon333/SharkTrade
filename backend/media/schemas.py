from pydantic import BaseModel


class NotAnImageResponse(BaseModel):
    detail: str = 'Not an image'


class MediaUUIDResponse(BaseModel):
    uuid: str
