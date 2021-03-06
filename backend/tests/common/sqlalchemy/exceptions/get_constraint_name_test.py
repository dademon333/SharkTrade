import pytest
from sqlalchemy.exc import DBAPIError

from common.sqlalchemy.exceptions import get_constraint_name


def test_simple_exception():
    text = '(sqlalchemy.dialects.postgresql.asyncpg.IntegrityError) ' \
           '<class \'asyncpg.exceptions.UniqueViolationError\'>: ' \
           'duplicate key value violates unique constraint "ix_users_username"'
    exc = DBAPIError(None, None, text)

    expected = 'ix_users_username'
    result = get_constraint_name(exc)
    assert result == expected


def test_no_constraint_name():
    text = 'abcdef'
    exc = DBAPIError(None, None, text)

    with pytest.raises(ValueError):
        get_constraint_name(exc)
