from sqlalchemy import select, func, insert
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import concat

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
            offset: int = 0
    ) -> list[Lot]:
        lots = await db.scalars(
            select(Lot)
            .where(Lot.is_canceled == False)  # noqa
            .order_by(Lot.id)
            .limit(limit)
            .offset(offset)
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
        item_id = create_instance.item_id
        owner_id = create_instance.owner_id
        lifetime = create_instance.lifetime_in_minutes

        await set_transaction_isolation_level(
            db, IsolationLevel.READ_UNCOMMITTED
        )

        await items.lock(db, item_id, owner_id)
        lot = await db.execute(
            insert(Lot)
            .values(
                owner_id=create_instance.owner_id,
                item_id=create_instance.item_id,
                end_time=func.now() + func.cast(concat(lifetime, ' MINUTES'), INTERVAL)
            )
        )
        return await self.get_by_id(db, lot.inserted_primary_key)


lots = CRUDLots(Lot)
