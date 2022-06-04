from pydantic import BaseModel


class MediaUUIDResponse(BaseModel):
    uuid: str


class NotAnImageResponse(BaseModel):
    detail: str = 'Not an image'


class MediaNotFoundResponse(BaseModel):
    detail: str = 'Media not found'


class PhotoNotFoundResponse(BaseModel):
    detail: str = 'Photo not found'
