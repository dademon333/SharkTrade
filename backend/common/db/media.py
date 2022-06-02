import uuid
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID, nullable=False, unique=True, default=uuid.uuid4)
    owner_id = Column(
        Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='SET NULL'),
        index=True
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())
