from fastapi import APIRouter

from auth.handlers import auth_router
from media.handlers import media_router
from stuff_handlers.handlers import stuff_router
from users.handlers import users_router

root_router = APIRouter()

root_router.include_router(stuff_router)
root_router.include_router(auth_router, tags=['Auth'])
root_router.include_router(
    users_router,
    prefix='/api/users',
    tags=['Users']
)

root_router.include_router(
    media_router,
    prefix='/api/media',
    tags=['Media']
)
