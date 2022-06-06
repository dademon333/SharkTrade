from fastapi import HTTPException, status

from common.db import ProfilePhoto
from common.responses import NotEnoughRightsResponse


def raise_if_no_access_to_edit_photo(
        photo: ProfilePhoto,
        user_id: int
) -> None:
    if photo.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=NotEnoughRightsResponse().detail
        )
