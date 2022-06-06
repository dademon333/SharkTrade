from pydantic import BaseModel


class OkResponse(BaseModel):
    response: str = 'ok'


class UnauthorizedResponse(BaseModel):
    detail: str = 'Not authenticated'


class AdminStatusRequiredResponse(BaseModel):
    detail: str = 'This operation requires minimum admin status'


class NotEnoughRightsResponse(BaseModel):
    detail: str = 'Not enough rights'


FOUND_NOT_ALLOWED_SYMBOLS = 'Found not allowed symbols: '
WHITESPACE_ONLY_FORBIDDEN = 'Whitespace only forbidden'
END_TIME_MUST_BE_GREATER_NOW = 'End time must be greater now'
