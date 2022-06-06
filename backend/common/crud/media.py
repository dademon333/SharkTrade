import re
import uuid
import aiofiles as aiof
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import Config
from .base import CRUDBase
from ..db import Media
from ..schemas.media import MediaCreate, MediaUpdate


class CRUDMedia(CRUDBase[Media, MediaCreate, MediaUpdate]):
    _UUID_PATTERN = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

    async def get_by_uuid(
            self,
            db: AsyncSession,
            uuid: str
    ) -> Media | None:
        if not self._UUID_PATTERN.fullmatch(uuid):
            raise ValueError

        result = await db.scalars(
            select(Media)
            .where(Media.uuid == uuid)
        )
        return result.first()

    @staticmethod
    async def save_on_disk(data: bytes) -> str:
        file_uuid = uuid.uuid4()
        path = Path(Config.MEDIA_ROOT, f'{file_uuid}.png')

        async with aiof.open(path, "wb") as file:
            await file.write(data)
            await file.flush()

        return str(file_uuid)


media = CRUDMedia(Media)
