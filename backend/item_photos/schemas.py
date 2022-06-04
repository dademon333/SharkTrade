from pydantic import BaseModel


class ItemPhotoAddForm(BaseModel):
    item_id: int
    media_uuid: str


class ReachedItemPhotosLimitResponse(BaseModel):
    detail: str = 'Reached item photos limit'
