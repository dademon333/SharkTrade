from fastapi import HTTPException, status
from sqlalchemy.exc import DBAPIError

from common.db import User
from common.sqlalchemy.exceptions import get_constraint_name
from .schemas import UserNotFoundResponse, EmailAlreadyExistsResponse, \
    UsernameAlreadyExistsResponse


def raise_if_user_not_exist(user: User | None) -> None:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=UserNotFoundResponse().detail
        )


def handle_user_constraint_conflict(exc: DBAPIError):
    constraint_name = get_constraint_name(exc)
    if 'email' in constraint_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=EmailAlreadyExistsResponse().detail
        )
    elif 'name' in constraint_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=UsernameAlreadyExistsResponse().detail
        )
    else:
        raise NotImplementedError(f'Not implemented handling of {constraint_name} constraint conflict')
