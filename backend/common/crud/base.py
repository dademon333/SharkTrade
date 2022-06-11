from typing import Generic, TypeVar, Type

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import insert, delete, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base for sql CRUD classes with default Create, Read, Update and Delete methods.

    Generic params:
    * ModelType: SQLAlchemy model class, which extends Base
    * CreateSchemaType: pydantic model with fields to create SQL item
    * UpdateSchemaType: pydantic model with fields to update SQL item

    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    # noinspection PyShadowingBuiltins
    async def get_by_id(
            self,
            db: AsyncSession,
            id: int
    ) -> ModelType | None:
        return await db.get(self.model, id)

    async def get_by_ids(
            self,
            db: AsyncSession,
            ids: list[int]
    ) -> list[ModelType]:
        result = await db.scalars(
            select(self.model)
            .where(self.model.id.in_(ids))
            .order_by(self.model.id)
        )
        return result.unique().all()

    async def get_many(
            self,
            db: AsyncSession,
            limit: int = 100,
            after_id: int | None = None
    ) -> list[ModelType]:
        where_clause = sqlalchemy.true()

        if after_id is not None:
            where_clause &= self.model.id > after_id

        result = await db.scalars(
            select(self.model)
            .where(where_clause)
            .order_by(self.model.id)
            .limit(limit)
        )
        return result.unique().all()

    async def get_all(
            self,
            db: AsyncSession
    ) -> list[ModelType]:
        result = await db.scalars(
            select(self.model)
            .order_by(self.model.id)
        )
        return result.unique().all()

    async def create(
            self,
            db: AsyncSession,
            create_instance: CreateSchemaType
    ) -> ModelType:
        result = await db.execute(
            insert(self.model)
            .values(**create_instance.dict())
        )
        return await self.get_by_id(db, result.inserted_primary_key)

    # noinspection PyShadowingBuiltins
    async def update(
            self,
            db: AsyncSession,
            id: int,
            update_instance: UpdateSchemaType
    ) -> ModelType:
        update_values = update_instance.dict(exclude_unset=True)
        if update_values != {}:
            await db.execute(
                update(self.model)
                .where(self.model.id == id)
                .values(**update_values)
            )
        return await self.get_by_id(db, id)

    # noinspection PyShadowingBuiltins
    async def delete(self, db: AsyncSession, id: int) -> None:
        await db.execute(
            delete(self.model)
            .where(self.model.id == id)
        )
