from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from common.db import User
from common.schemas.users import UserCreate, UserUpdate
from common.security.users import hash_password
from .base import CRUDBase


class CRUDUsers(CRUDBase[User, UserCreate, UserUpdate]):
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        user = await db.scalars(
            select(User)
            .where(User.email == func.lower(email))
        )
        return user.first()

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> User | None:
        user = await db.scalars(
            select(User)
            .where(User.username == func.lower(username))
        )
        return user.first()

    @staticmethod
    async def get_by_username_or_email(db: AsyncSession, username: str) -> User | None:
        user = await db.scalars(
            select(User)
            .where(
                (User.username == func.lower(username))
                | (User.email == func.lower(username))
            )
        )
        return user.first()

    # noinspection PyShadowingBuiltins
    async def update(
            self,
            db: AsyncSession,
            id: int,
            update_instance: UserUpdate
    ) -> User:
        if update_instance.password is not None:
            update_instance.password = hash_password(id, update_instance.password)
        return await super().update(db, id, update_instance)

    async def create(
            self,
            db: AsyncSession,
            create_instance: UserCreate
    ) -> User:
        result = await super().create(db, create_instance)
        return await self.update(
            db,
            result.id,
            UserUpdate(password=create_instance.password)
        )


users = CRUDUsers(User)
