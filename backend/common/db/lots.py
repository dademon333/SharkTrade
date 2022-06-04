from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, func
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
    is_canceled = Column(Boolean, nullable=False, server_default='false')
    is_withdrawn = Column(Boolean, nullable=False, server_default='false')
    win_bid_id = Column(Integer, index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    end_time = Column(DateTime, nullable=False)

    bids = relationship('Bid', lazy='joined', backref='lot')
