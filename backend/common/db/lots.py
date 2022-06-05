from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .base import Base


class Lot(Base):
    __tablename__ = 'lots'

    id = Column(Integer, primary_key=True)
    owner_id = Column(
        Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='SET NULL'),
        index=True
    )
    item_id = Column(
        Integer,
        ForeignKey('items.id', onupdate='CASCADE', ondelete='SET NULL'),
        index=True
    )
    is_canceled = Column(Boolean, nullable=False, index=True, server_default='false')
    win_bid_id = Column(Integer, index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    end_time = Column(DateTime, nullable=False)

    bids = relationship('Bid', lazy='joined', backref='lot')

    @hybrid_property
    def win_bid(self):
        if self.win_bid_id is None:
            return None

        win_bid = [x for x in self.bids if x.id == self.win_bid_id]
        if win_bid == []:
            return None
        return win_bid[0]

    @hybrid_property
    def max_bid(self) -> int:
        return max([x.amount for x in self.bids], default=0)
