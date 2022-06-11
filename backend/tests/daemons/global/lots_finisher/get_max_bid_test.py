from common.db import Bid
from daemons.global_daemons.lots_finisher import LotsFinisher


def test_one_bid():
    bids = [Bid(id=1, amount=1000)]
    result = LotsFinisher._get_max_bid(bids)
    assert result == bids[0]


def test_much_bids():
    bids = [
        Bid(id=1, amount=1000),
        Bid(id=2, amount=2000),
        Bid(id=3, amount=3000)
    ]
    result = LotsFinisher._get_max_bid(bids)
    assert result == bids[-1]
