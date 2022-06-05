from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from ..db import Item
from ..schemas.items import ItemUpdate, ItemCreate


class CRUDItems(CRUDBase[Item, ItemCreate, ItemUpdate]):
    @staticmethod
    async def get_by_owner_id(
            db: AsyncSession,
            owner_id: int,
            limit: int = 25,
            offset: int = 0
    ) -> list[Item]:
        items = await db.scalars(
            select(Item)
            .where(Item.owner_id == owner_id)
            .order_by(Item.id)
            .limit(limit)
            .offset(offset)
        )
        return items.unique().all()

    @staticmethod
    async def get_user_items_count(
            db: AsyncSession,
            owner_id: int
    ) -> int:
        count = await db.scalars(
            select(func.count(Item.id))
            .where(Item.owner_id == owner_id)
        )
        return count.first()

    @staticmethod
    async def lock(
            db: AsyncSession,
            item_id: int,
            owner_id: int
    ) -> None:
        """Locks item.

        Raises AssertionError, if item is already locked
        or was transferred to another account.

        """
        result = await db.execute(
            update(Item)
            .where(
                (Item.id == item_id)
                & (Item.owner_id == owner_id)
                & (Item.is_locked == False)  # noqa
            )
            .values(is_locked=True)
        )
        assert result.rowcount == 1

    @staticmethod
    async def unlock(db: AsyncSession, item_id: int) -> None:
        await db.execute(
            update(Item)
            .where((Item.id == item_id))
            .values(is_locked=False)
        )


items = CRUDItems(Item)
