from datetime import datetime

from pydantic import BaseModel, Field

from common.db import UserStatus


nickname_pattern = r'\A[a-zA-Z0-9]{4,30}\Z'
email_pattern = r'\A[a-zA-Z0-9]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+\Z'


class UserCreate(BaseModel):
    nickname: str = Field(..., regex=nickname_pattern)
    email: str = Field(..., regex=email_pattern, max_length=40)
    password: str = Field(..., min_length=8, max_length=30)


class UserUpdate(BaseModel):
    nickname: str | None = Field(None, regex=nickname_pattern)
    email: str | None = Field(None, regex=email_pattern, max_length=40)
    password: str | None = Field(None, min_length=8, max_length=30)


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
