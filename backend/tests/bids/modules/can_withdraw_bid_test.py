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


def test_highest_bid():
    lot = Lot()
    bids = [
        Bid(id=1, amount=1000, lot=lot),
        Bid(id=2, amount=2000, lot=lot),
        Bid(id=3, amount=3000, lot=lot)
    ]
    lot.bids = bids

    result = can_withdraw_bid(bids[2])
    assert result is False


def test_not_highest_bid():
    lot = Lot()
    bids = [
        Bid(id=1, amount=1000, lot=lot),
        Bid(id=2, amount=2000, lot=lot),
        Bid(id=3, amount=3000, lot=lot)
    ]
    lot.bids = bids

    result = can_withdraw_bid(bids[0])
    assert result is True


def test_lost_bid():
    lot = Lot(win_bid_id=3)
    bids = [
        Bid(id=1, amount=1000, lot=lot),
        Bid(id=2, amount=2000, lot=lot),
        Bid(id=3, amount=3000, lot=lot)
    ]
    lot.bids = bids

    result = can_withdraw_bid(bids[0])
    assert result is True
