import json
from typing import AsyncIterator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from config import Config
from tokens import Tokens
from ..json import json_serializer, json_deserializer

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

engine = create_async_engine(
    Tokens.SQLALCHEMY_POSTGRESQL_URL,
    future=True,
    echo=Config.DEBUG,
    json_serializer=lambda obj: json.dumps(obj, default=json_serializer, ensure_ascii=False),
    json_deserializer=lambda obj: json.loads(obj, object_pairs_hook=json_deserializer)
)
session_factory = sessionmaker(bind=engine, class_=AsyncSession)
metadata = MetaData(bind=engine, naming_convention=naming_convention)

Base = declarative_base(metadata=metadata)


def get_enum_values(enum):
    """Returns a list of enum values.

    Problem: SQLAlchemy uses names of enum's values to store in database instead of it's values
    e.g.:
    class UserStatus(enum.Enum):
        USER = 'user'
        MODER = 'moderator'
        ADMIN = 'administrator'
    will be converted to ['USER', 'MODER', 'ADMIN']
    Expected: ['user', 'moderator', 'administrator']

    Solution: pass this func to values_callable arg of sqlalchemy.Enum
    class User(Base):
        ...
        status = Column(Enum(UserStatus, values_callable=get_enum_values))
        ...

    https://stackoverflow.com/a/55160320

    """
    return [x.value for x in enum]


async def get_db() -> AsyncIterator[AsyncSession]:
    session = session_factory()
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
