from sqlalchemy import Integer, Column, ForeignKey, DateTime, func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from ..db import Base


class ProfilePhoto(Base):
    __tablename__ = 'profile_photos'

    id = Column(Integer, primary_key=True)
    owner_id = Column(
        Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
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
