from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .items import items
from .base import CRUDBase
from ..db import Lot
from ..schemas.lots import LotCreate, LotUpdate
from ..sqlalchemy.transaction import set_transaction_isolation_level, IsolationLevel


class CRUDLots(CRUDBase[Lot, LotCreate, LotUpdate]):
    @staticmethod
    async def get_active(
            db: AsyncSession,
            limit: int = 25,
            before_id: int | None = None
    ) -> list[Lot]:
        where_clause = Lot.is_canceled == False  # noqa
        if before_id is not None:
            where_clause &= (Lot.id < before_id)

        lots = await db.scalars(
            select(Lot)
            .where(where_clause)
            .order_by(Lot.id.desc())  # noqa
            .limit(limit)
        )
        return lots.unique().all()

    @staticmethod
    async def get_active_count(db: AsyncSession) -> int:
        count = await db.scalars(
            select(func.count(Lot.id))
            .where(Lot.is_canceled == False)  # noqa
        )
        return count.first()

    @staticmethod
    async def get_by_owner_id(
            db: AsyncSession,
            owner_id: int,
            limit: int = 25,
            offset: int = 0
    ) -> list[Lot]:
        items = await db.scalars(
            select(Lot)
            .where(Lot.owner_id == owner_id)
            .order_by(Lot.id)
            .limit(limit)
            .offset(offset)
        )
        return items.unique().all()

    @staticmethod
    async def get_user_lots_count(
            db: AsyncSession,
            owner_id: int
    ) -> int:
        count = await db.scalars(
            select(func.count(Lot.id))
            .where(Lot.owner_id == owner_id)
        )
        return count.first()

    async def create(
            self,
            db: AsyncSession,
            create_instance: LotCreate
    ) -> Lot:
        await set_transaction_isolation_level(
            db, IsolationLevel.READ_UNCOMMITTED
        )
        await items.lock(db, create_instance.item_id, create_instance.owner_id)
        return await super().create(db, create_instance)


lots = CRUDLots(Lot)
