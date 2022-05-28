from fastapi import APIRouter, File, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common import crud
from common.db import get_db
from common.responses import UnauthorizedResponse
from common.schemas.media import MediaCreate
from common.security.auth import get_user_id, check_auth
from .modules import validate_image
from .schemas import NotAnImageResponse, MediaUUIDResponse

media_router = APIRouter()


@media_router.post(
    '',
    response_model=MediaUUIDResponse,
    responses={
        400: {'model': NotAnImageResponse},
        401: {'model': UnauthorizedResponse}
    },
    dependencies=[Depends(check_auth)]
)
async def upload_image(
        db: AsyncSession = Depends(get_db),
        owner_id: int = Depends(get_user_id),
        file: bytes = File(..., max_length=10_485_760)  # 10 MB max
):
    """Сохраняет изображение на сервере и возвращает его uuid."""
    if not validate_image(file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NotAnImageResponse().detail
        )

    uuid = await crud.media.save_on_disk(file)
    await crud.media.create(db, MediaCreate(uuid=uuid, owner_id=owner_id))
    return MediaUUIDResponse(uuid=uuid)
