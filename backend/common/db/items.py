from sqlalchemy import Column, Integer, ForeignKey, \
    String, Text, Boolean, DateTime, func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

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
    photo_id = Column(
        Integer,
        ForeignKey('media.id', onupdate='CASCADE'),
        nullable=False,
        index=True
    )
    is_locked = Column(Boolean, nullable=False, server_default='false')
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    media = relationship(
        'Media',
        lazy='joined',
        foreign_keys=[photo_id],
        uselist=False
    )
    media_uuid = association_proxy('media', 'uuid')
