from pydantic import BaseModel


class LoginErrorResponse(BaseModel):
    detail: str = 'Invalid email or password'


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
