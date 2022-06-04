from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from common import crud
from common.db import get_db
from common.responses import OkResponse, UnauthorizedResponse, \
    NotEnoughRightsResponse
from common.schemas.profile_photos import ProfilePhotoCreate, ProfilePhotoInfo
from common.security.auth import get_user_id
from media.modules import raise_if_media_not_exist, raise_if_photo_not_exist
from media.schemas import MediaNotFoundResponse, PhotoNotFoundResponse
from .modules import raise_if_no_access_to_edit_photo

profile_photos_router = APIRouter()


@profile_photos_router.post(
    '',
    response_model=ProfilePhotoInfo,
    responses={
        401: {'model': UnauthorizedResponse},
        404: {'model': MediaNotFoundResponse}
    }
)
async def set_profile_photo(
        media_uuid: str = Body(..., embed=True),
        user_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Устанавливает фотографию профиля."""
    try:
        media = await crud.media.get_by_uuid(db, media_uuid)
    except ValueError:
        media = None
    raise_if_media_not_exist(media)

    user = await crud.users.get_by_id(db, user_id)
    already_have_this_photo = [x for x in user.profile_photos if x.media_uuid == media_uuid]
    if already_have_this_photo == []:
        photo = await crud.profile_photos.create(
            db,
            ProfilePhotoCreate(owner_id=user_id, media_id=media.id)
        )
    else:
        photo = await crud.profile_photos.update_id(db, already_have_this_photo[0].id)

    return ProfilePhotoInfo.from_orm(photo)


@profile_photos_router.delete(
    '/{photo_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': NotEnoughRightsResponse},
        404: {'model': PhotoNotFoundResponse}
    }
)
async def delete_profile_photo(
        photo_id: int,
        user_id: int = Depends(get_user_id),
        db: AsyncSession = Depends(get_db)
):
    """Удаляет фотографию профиля по её идентификатору."""
    photo = await crud.profile_photos.get_by_id(db, photo_id)
    raise_if_photo_not_exist(photo)
    raise_if_no_access_to_edit_photo(photo, user_id)
    await crud.profile_photos.delete(db, photo.id)
    return OkResponse()
