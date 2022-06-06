import sqlalchemy.exc
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from ..db import ItemPhoto
from ..schemas.item_photos import ItemPhotoCreate, ItemPhotoUpdate
from ..sqlalchemy.transaction import set_transaction_isolation_level, IsolationLevel


class CRUDItemPhotos(CRUDBase[ItemPhoto, ItemPhotoCreate, ItemPhotoUpdate]):
    async def create(
            self,
            db: AsyncSession,
            create_instance: ItemPhotoCreate
    ) -> ItemPhoto:
        await set_transaction_isolation_level(
            db, IsolationLevel.READ_UNCOMMITTED
        )

        item_photo = await super().create(db, create_instance)
        photos_count = await self.get_item_photos_count(
            db, create_instance.item_id
        )
        if photos_count > 10:
            raise sqlalchemy.exc.IntegrityError(None, None, None)

        return item_photo

    @staticmethod
    async def get_item_photos_count(
            db: AsyncSession,
            item_id: int
    ) -> int:
        count = await db.scalars(
            select(func.count(ItemPhoto.id))
            .where(ItemPhoto.item_id == item_id)
        )
        return count.first()


item_photos = CRUDItemPhotos(ItemPhoto)
