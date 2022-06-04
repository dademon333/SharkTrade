from fastapi import HTTPException, status

from common.db import Item, UserStatus
from common.responses import NotEnoughRightsResponse
from .schemas import ItemNotFoundResponse


def raise_if_item_not_exist(item: Item | None) -> None:
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ItemNotFoundResponse().detail
        )


def raise_if_no_access_to_edit_item(
        item: Item,
        user_id: int,
        user_status: UserStatus
) -> None:
    if item.owner_id != user_id and user_status != UserStatus.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=NotEnoughRightsResponse().detail
        )
