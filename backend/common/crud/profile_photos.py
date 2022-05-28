from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from common.db import ProfilePhoto
from common.schemas.profile_photos import ProfilePhotoCreate, ProfilePhotoUpdate
from .base import CRUDBase


class CRUDProfilePhotos(CRUDBase[ProfilePhoto, ProfilePhotoCreate, ProfilePhotoUpdate]):
    # noinspection PyShadowingBuiltins
    async def update_id(
            self,
            db: AsyncSession,
            id: int
    ) -> None:
        """Update profile photo id to next autoincrement value."""
        # Bind next autoincrement id
        photo = await self.get_by_id(db, id)
        temp = await self.create(db, ProfilePhotoCreate(owner_id=photo.owner_id, media_id=photo.media_id))
        await self.delete(db, temp.id)

        # Update current photo id
        await db.execute(
            update(ProfilePhoto)
            .where(ProfilePhoto.id == id)
            .values({'id': temp.id})
        )


profile_photos = CRUDProfilePhotos(ProfilePhoto)
