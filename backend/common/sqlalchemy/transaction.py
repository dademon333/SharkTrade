from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession


class IsolationLevel(Enum):
    AUTOCOMMIT = 'AUTOCOMMIT'
    READ_UNCOMMITTED = 'READ UNCOMMITTED'
    READ_COMMITTED = 'READ COMMITTED'
    REPEATABLE_READ = 'REPEATABLE READ'
    SERIALIZABLE = 'SERIALIZABLE'


async def set_transaction_isolation_level(db: AsyncSession, level: IsolationLevel):
    await db.connection(
        execution_options={'isolation_level': level.value}
    )
