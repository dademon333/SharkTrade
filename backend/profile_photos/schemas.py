from pydantic import BaseModel


class MediaNotFoundResponse(BaseModel):
    detail: str = 'Media not found'


class PhotoNotFoundResponse(BaseModel):
    detail: str = 'Photo not found'
