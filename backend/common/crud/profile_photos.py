from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from ..db import ProfilePhoto
from ..schemas.profile_photos import ProfilePhotoCreate, ProfilePhotoUpdate


class CRUDProfilePhotos(CRUDBase[ProfilePhoto, ProfilePhotoCreate, ProfilePhotoUpdate]):
    # noinspection PyShadowingBuiltins
    async def update_id(
            self,
            db: AsyncSession,
            id: int
    ) -> ProfilePhoto:
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
        return photo


profile_photos = CRUDProfilePhotos(ProfilePhoto)
