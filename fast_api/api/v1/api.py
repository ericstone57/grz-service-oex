from fastapi import APIRouter

from .endpoints import config

api_router = APIRouter()
api_router.include_router(config.router, prefix='/config', tags=["Config"])

