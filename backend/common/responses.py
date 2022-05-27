from pydantic import BaseModel


class OkResponse(BaseModel):
    response: str = 'ok'


class UnauthorizedResponse(BaseModel):
    detail: str = 'Not authenticated'


class AdminStatusRequiredResponse(BaseModel):
    detail: str = 'This operation requires minimum admin status'
