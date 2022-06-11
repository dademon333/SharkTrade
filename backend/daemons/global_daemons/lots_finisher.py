import asyncio
import traceback

from sqlalchemy.ext.asyncio import AsyncSession

from common import crud
from common.db import Lot, Bid, session_factory
from common.schemas.items import ItemUpdate
from common.schemas.lots import LotUpdate


class LotsFinisher:
    """Sums up the lots if reached end_time."""
    @classmethod
    async def run(cls):
        db = session_factory(expire_on_commit=False)
        while True:
            lots = await crud.lots.get_ready_for_finish(db)
            for lot in lots:
                try:
                    await cls._finish_lot(db, lot)
                    await db.commit()
                except:
                    traceback.print_exc()
                    await db.rollback()
                    await cls._close_lot_without_winner(db, lot.id)

            await asyncio.sleep(1)

    @classmethod
    async def _finish_lot(cls, db: AsyncSession, lot: Lot) -> None:
        bids = lot.bids
        if bids == []:
            await cls._close_lot_without_winner(db, lot.id)
            return

        max_bid = cls._get_max_bid(bids)
        await crud.lots.update(
            db,
            lot.id,
            LotUpdate(is_cancelled=True, win_bid_id=max_bid.id)
        )
        await crud.items.update(
            db,
            lot.item_id,
            ItemUpdate(owner_id=max_bid.owner_id, is_locked=False)
        )
        await crud.users.increment_balance(
            db,
            lot.owner_id,
            increment=max_bid.amount
        )

    @classmethod
    async def _close_lot_without_winner(
            cls,
            db: AsyncSession,
            lot_id: int
    ) -> None:
        await crud.lots.update(
            db,
            lot_id,
            LotUpdate(is_cancelled=True, win_bid_id=None)
        )

    @classmethod
    def _get_max_bid(cls, bids: list[Bid]) -> Bid:
        return max(bids, key=lambda x: x.amount)
