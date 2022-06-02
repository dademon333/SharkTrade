from pydantic import BaseModel


class UsernameAlreadyExistsResponse(BaseModel):
    detail: str = 'Username already exists'


class EmailAlreadyExistsResponse(BaseModel):
    detail: str = 'Email already exists'


class UserNotFoundResponse(BaseModel):
    detail: str = 'User not found'
