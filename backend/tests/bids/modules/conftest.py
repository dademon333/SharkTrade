import pytest

from common.db import Bid, Lot


@pytest.fixture()
def bids_factory():
    def _bids_factory(lot: Lot | None = None):
        if lot is None:
            lot = Lot()
        bids = [
            Bid(id=1, amount=1000, lot=lot),
            Bid(id=2, amount=2000, lot=lot),
            Bid(id=3, amount=3000, lot=lot)
        ]
        lot.bids = bids
        return bids

    return _bids_factory
