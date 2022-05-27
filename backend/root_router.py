from fastapi import APIRouter

from auth.handlers import auth_router
from stuff_handlers.handlers import stuff_router

root_router = APIRouter()

root_router.include_router(stuff_router)
root_router.include_router(auth_router, tags=['Auth'])
