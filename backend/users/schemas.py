from pydantic import BaseModel


class NicknameAlreadyExistsResponse(BaseModel):
    detail: str = 'Nickname already exists'


class EmailAlreadyExistsResponse(BaseModel):
    detail: str = 'Email already exists'


class UserNotFoundResponse(BaseModel):
    detail: str = 'User not found'
