import uuid
import aiofiles as aiof
from pathlib import Path

from common.db import Media
from common.schemas.media import MediaCreate, MediaUpdate
from config import Config
from .base import CRUDBase


class CRUDMedia(CRUDBase[Media, MediaCreate, MediaUpdate]):
    @staticmethod
    async def save_on_disk(data: bytes) -> str:
        file_uuid = uuid.uuid4()
        path = Path(Config.MEDIA_ROOT, f'{file_uuid}.png')

        async with aiof.open(path, "wb") as file:
            await file.write(data)
            await file.flush()

        return str(file_uuid)


media = CRUDMedia(Media)
