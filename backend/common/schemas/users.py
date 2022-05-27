from datetime import datetime

from pydantic import BaseModel, Field

from common.db import UserStatus


class UserCreate(BaseModel):
    nickname: str = Field(..., min_length=4, max_length=20)
    email: str = Field(..., regex=r'\A[a-zA-Z0-9]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+\Z')
    password: str = Field(..., min_length=8, max_length=30)
    status: UserStatus


class UserUpdate(BaseModel):
    nickname: str | None = Field(None, min_length=4, max_length=20)
    email: str | None = Field(None, regex=r'\A[a-zA-Z0-9]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+\Z')
    password: str | None = Field(None, min_length=8, max_length=30)
    status: UserStatus | None = None


class UserInfoBase(BaseModel):
    id: int
    nickname: str
    email: str
    status: UserStatus

    class Config:
        orm_mode = True


class UserInfo(UserInfoBase):
    pass


class UserInfoExtended(UserInfoBase):
    created_at: datetime
