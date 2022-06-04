import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from common import crud
from common.db import get_db, UserStatus
from common.responses import UnauthorizedResponse, NotEnoughRightsResponse, \
    OkResponse
from common.schemas.item_photos import ItemPhotoCreate, ItemPhotoInfo
from common.security.auth import get_user_id, get_user_status
from items.modules import raise_if_item_not_exist, raise_if_no_access_to_edit_item
from items.schemas import ItemNotFoundResponse
from media.modules import raise_if_media_not_exist, raise_if_photo_not_exist
from media.schemas import MediaNotFoundResponse, PhotoNotFoundResponse
from .schemas import ItemPhotoAddForm, ReachedItemPhotosLimitResponse

item_photos_router = APIRouter()


@item_photos_router.post(
    '',
    response_model=ItemPhotoInfo,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': NotEnoughRightsResponse},
        404: {'model': MediaNotFoundResponse | ItemNotFoundResponse},
        409: {'model': ReachedItemPhotosLimitResponse}
    }
)
async def add_item_photo(
        add_form: ItemPhotoAddForm,
        user_id: int = Depends(get_user_id),
        user_status: UserStatus = Depends(get_user_status),
        db: AsyncSession = Depends(get_db)
):
    """Добавляет фотографию предмета."""
    try:
        media = await crud.media.get_by_uuid(db, add_form.media_uuid)
    except ValueError:
        media = None
    raise_if_media_not_exist(media)

    item = await crud.items.get_by_id(db, add_form.item_id)
    raise_if_item_not_exist(item)
    raise_if_no_access_to_edit_item(item, user_id, user_status)

    try:
        photo = await crud.item_photos.create(
            db,
            ItemPhotoCreate(item_id=item.id, media_id=media.id)
        )
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ReachedItemPhotosLimitResponse().detail
        )

    return ItemPhotoInfo.from_orm(photo)


@item_photos_router.delete(
    '/{photo_id}',
    response_model=OkResponse,
    responses={
        401: {'model': UnauthorizedResponse},
        403: {'model': NotEnoughRightsResponse},
        404: {'model': PhotoNotFoundResponse}
    }
)
async def delete_item_photo(
        photo_id: int,
        user_id: int = Depends(get_user_id),
        user_status: UserStatus = Depends(get_user_status),
        db: AsyncSession = Depends(get_db)
):
    """Удаляет фотографию предмета."""
    photo = await crud.item_photos.get_by_id(db, photo_id)
    raise_if_photo_not_exist(photo)
    raise_if_no_access_to_edit_item(photo.item, user_id, user_status)
    await crud.item_photos.delete(db, photo.id)
    return OkResponse()
