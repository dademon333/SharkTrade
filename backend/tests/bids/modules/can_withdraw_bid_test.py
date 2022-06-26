from typing import Callable

from bids.modules import can_withdraw_bid
from common.db import Bid, Lot


def test_withdrawn():
    bid = Bid(is_withdrawn=True)
    result = can_withdraw_bid(bid)
    assert result is False


def test_win_bid():
    lot = Lot(win_bid_id=1)
    bid = Bid(id=1, lot=lot)
    result = can_withdraw_bid(bid)
    assert result is False


def test_highest_bid(bids_factory: Callable[..., list[Bid]]):
    bids = bids_factory()
    result = can_withdraw_bid(bids[-1])
    assert result is False


def test_not_highest_bid(bids_factory: Callable[..., list[Bid]]):
    bids = bids_factory()
    result = can_withdraw_bid(bids[0])
    assert result is True


def test_lost_bid(bids_factory: Callable[..., list[Bid]]):
    lot = Lot(win_bid_id=3)
    bids = bids_factory(lot)
    result = can_withdraw_bid(bids[0])
    assert result is True


def test_force_cancelled_lot(bids_factory: Callable[..., list[Bid]]):
    lot = Lot(win_bid_id=None, is_cancelled=True)
    bids = bids_factory(lot)

    for bid in bids:
        result = can_withdraw_bid(bid)
        assert result is True
