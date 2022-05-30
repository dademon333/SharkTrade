import enum

from sqlalchemy import Column, Integer, DateTime, func, \
    Index, text, String, Enum
from sqlalchemy.orm import relationship

from .base import Base, get_enum_values


class UserStatus(str, enum.Enum):
    USER = 'user'
    ADMIN = 'admin'


user_status_weights = {
    None: 0,
    UserStatus.USER: 0,
    UserStatus.ADMIN: 100
}


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    status = Column(
        Enum(UserStatus, name='user_status', values_callable=get_enum_values),
        nullable=False,
        server_default=UserStatus.USER
    )
    rubles_balance = Column(Integer, nullable=False, server_default='0')
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    profile_photos = relationship('ProfilePhoto', lazy='joined')

    __table_args__ = (
        Index('ix_users_email', text('LOWER(email)'), unique=True),
        Index('ix_users_username', text('LOWER(username)'), unique=True)
    )
