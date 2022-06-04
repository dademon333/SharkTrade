from datetime import datetime

from pydantic import BaseModel, Field

from .profile_photos import ProfilePhotoInfo
from ..db import UserStatus

username_pattern = r'\A[a-zA-Z0-9_]{4,30}\Z'
email_pattern = r'\A[a-zA-Z0-9]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+\Z'


class UserCreate(BaseModel):
    username: str = Field(..., regex=username_pattern)
    email: str = Field(..., regex=email_pattern, max_length=40)
    password: str = Field(..., min_length=8, max_length=30)


class UserUpdate(BaseModel):
    username: str | None = Field(None, regex=username_pattern)
    email: str | None = Field(None, regex=email_pattern, max_length=40)
    password: str | None = Field(None, min_length=8, max_length=30)


class UserInfo(BaseModel):
    id: int
    username: str
    status: UserStatus
    profile_photos: list[ProfilePhotoInfo]

    class Config:
        orm_mode = True


class UserInfoExtended(UserInfo):
    email: str
    rubles_balance: int
    created_at: datetime
