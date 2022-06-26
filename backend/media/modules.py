import io

from PIL import Image
from fastapi import HTTPException, status

from common.db import Media, Base
from .schemas import MediaNotFoundResponse, PhotoNotFoundResponse


def raise_if_media_not_exists(media: Media) -> None:
    if media is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=MediaNotFoundResponse().detail
        )


def raise_if_photo_not_exists(photo: Base) -> None:
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PhotoNotFoundResponse().detail
        )


def validate_image(image_data: bytes) -> bool:
    """Returns True, if image_data is a valid image, else - False."""
    try:
        image = Image.open(io.BytesIO(image_data))
        image.verify()
        # .verify() has side-effects, we have to reload data
        image = Image.open(io.BytesIO(image_data))
        image.transpose(Image.FLIP_LEFT_RIGHT)
        return True
    except:
        return False
