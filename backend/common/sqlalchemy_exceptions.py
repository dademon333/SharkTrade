import re

from sqlalchemy.exc import DBAPIError


_CONSTRAINT_PATTERN = re.compile(r'constraint "(?P<name>[a-zA-Z0-9_]+)"')


def get_constraint_name(exception: DBAPIError) -> str:
    """Returns name of conflict constraint in SQLAlchemy exception.

    Actually works only with Unique constraint (maybe, other not checked).

    """
    message = exception._message().split('\n')[0]
    match = _CONSTRAINT_PATTERN.search(message)
    if match is None:
        raise ValueError(f'Can\'t find constraint name in {exception._message()}')
    return match.groupdict()['name']
