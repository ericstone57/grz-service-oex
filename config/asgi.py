import os
import sys
from pathlib import Path

import aioredis
import environ
from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.middleware.cors import CORSMiddleware

env = environ.Env()
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "grz_service_oex"))
if env('APP_ENV', default='local') == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

API_PREFIX = f'/api/{env("API_VERSION")}/{env("API_PREFIX")}'

django_application = get_wsgi_application()

fastapp = FastAPI(
    openapi_url=f'{API_PREFIX}/openapi.json',
    docs_url=f'{API_PREFIX}/docs'
)

from fast_api.api.v1.api import api_router

fastapp.include_router(api_router, prefix=API_PREFIX)

fastapp.mount('/app', WSGIMiddleware(django_application))
fastapp.add_middleware(
    CORSMiddleware,
    allow_origins=env.list('BACKEND_CORS_ORIGINS', default=['']),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@fastapp.on_event("startup")
async def startup():
    redis = aioredis.from_url(env('REDIS_URL'), encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="api_cache")
