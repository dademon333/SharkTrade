from fastapi import APIRouter

from auth.handlers import auth_router
from media.handlers import media_router
from profile_photos.handlers import profile_photos_router
from stuff_handlers.handlers import stuff_router
from users.handlers import users_router
from web_sockets.handlers import websockets_router

root_router = APIRouter()

root_router.include_router(stuff_router)
root_router.include_router(auth_router, tags=['Auth'])

root_router.include_router(
    websockets_router,
    prefix='/ws',
    tags=['Websockets']
)

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

root_router.include_router(
    profile_photos_router,
    prefix='/api/profile_photos',
    tags=['Profile photos']
)
