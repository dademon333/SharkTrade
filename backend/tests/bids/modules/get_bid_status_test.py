from bids.modules import get_bid_status
from common.db import Bid, Lot
from common.schemas.bids import BidStatus


def test_one_bid():
    lot = Lot(win_bid_id=1)
    bid = Bid(id=1, lot=lot)
    assert get_bid_status(bid) == BidStatus.WIN


def test_win_bid():
    lot = Lot(win_bid_id=3)
    bids = [
        Bid(id=1, amount=1000, lot=lot),
        Bid(id=2, amount=2000, lot=lot),
        Bid(id=3, amount=3000, lot=lot)
    ]
    lot.bids = bids
    assert get_bid_status(bids[2]) == BidStatus.WIN


def test_highest_bid():
    lot = Lot()
    bids = [
        Bid(id=1, amount=1000, lot=lot),
        Bid(id=2, amount=2000, lot=lot),
        Bid(id=3, amount=3000, lot=lot)
    ]
    lot.bids = bids
    assert get_bid_status(bids[2]) == BidStatus.HIGHEST


def test_not_highest_bid():
    lot = Lot()
    bids = [
        Bid(id=1, amount=1000, lot=lot),
        Bid(id=2, amount=2000, lot=lot),
        Bid(id=3, amount=3000, lot=lot)
    ]
    lot.bids = bids
    assert get_bid_status(bids[1]) == BidStatus.LOSE


def test_lowest_bid():
    lot = Lot()
    bids = [
        Bid(id=1, amount=1000, lot=lot),
        Bid(id=2, amount=2000, lot=lot),
        Bid(id=3, amount=3000, lot=lot)
    ]
    lot.bids = bids
    assert get_bid_status(bids[0]) == BidStatus.LOSE
