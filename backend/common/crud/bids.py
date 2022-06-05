from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from ..db import Bid
from ..schemas.bids import BidCreate, BidUpdate


class CRUDBids(CRUDBase[Bid, BidCreate, BidUpdate]):
    @staticmethod
    async def get_by_owner_id(
            db: AsyncSession,
            user_id: int,
            limit: int = 25,
            offset: int = 0
    ) -> list[Bid]:
        bids = await db.scalars(
            select(Bid)
            .where(Bid.owner_id == user_id)
            .order_by(Bid.id)
            .limit(limit)
            .offset(offset)
        )
        return bids.unique().all()

    @staticmethod
    async def get_user_bids_count(
            db: AsyncSession,
            user_id: int
    ) -> int:
        count = await db.scalars(
            select(func.count(Bid.id))
            .where(Bid.owner_id == user_id)
        )
        return count.first()

    @staticmethod
    async def set_is_withdrawn(
            db: AsyncSession,
            bid_id: int
    ) -> None:
        """Set is_withdrawn to True.

        If bid already withdrawn, raises AssertionError.

        """
        is_updated = await db.execute(
            update(Bid)
            .where(
                (Bid.id == bid_id)
                & (Bid.is_withdrawn == False)  # noqa
            )
            .values(is_withdrawn=True)
        )
        assert is_updated.rowcount == 1


bids = CRUDBids(Bid)
