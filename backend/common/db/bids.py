from sqlalchemy import Integer, Column, ForeignKey, DateTime, func, Boolean

from .base import Base


class Bid(Base):
    __tablename__ = 'bids'

    id = Column(Integer, primary_key=True)
    owner_id = Column(
        Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='SET NULL'),
        index=True
    )
    lot_id = Column(
        Integer,
        ForeignKey('lots.id', onupdate='CASCADE', ondelete='SET NULL'),
        index=True
    )
    amount = Column(Integer, nullable=False)
    is_withdrawn = Column(Boolean, nullable=False, server_default='false')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
