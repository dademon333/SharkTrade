from pydantic import BaseModel


class ReachedItemPhotosLimitResponse(BaseModel):
    detail: str = 'Reached item photos limit'
