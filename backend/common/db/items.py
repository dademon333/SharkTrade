from sqlalchemy import Column, Integer, ForeignKey, \
    String, Text, Boolean, DateTime, func
from sqlalchemy.orm import relationship, backref

from .base import Base


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    owner_id = Column(
        Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='SET NULL'),
        index=True
    )
    name = Column(String, nullable=False)
    description = Column(Text)
    is_locked = Column(Boolean, nullable=False, server_default='false')
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    photos = relationship(
        'ItemPhoto',
        lazy='joined',
        backref=backref('item', lazy='joined', uselist=False)
    )
