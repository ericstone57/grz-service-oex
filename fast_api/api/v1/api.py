from fastapi import APIRouter

from .endpoints import config, banner, space, exhibition

api_router = APIRouter()
api_router.include_router(config.router, prefix='/config', tags=["Config"])
api_router.include_router(banner.router, prefix='/banner', tags=["Banner"])
api_router.include_router(space.router, prefix='/space', tags=["Space"])
api_router.include_router(exhibition.router, prefix='/exhibition', tags=["Exhibition"])
