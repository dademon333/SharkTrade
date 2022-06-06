from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from .base import Base


class ItemPhoto(Base):
    __tablename__ = 'item_photos'

    id = Column(Integer, primary_key=True)
    item_id = Column(
        Integer,
        ForeignKey('items.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    media_id = Column(
        Integer,
        ForeignKey('media.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    media = relationship('Media', lazy='joined', foreign_keys=[media_id], uselist=False)
    media_uuid = association_proxy('media', 'uuid')
