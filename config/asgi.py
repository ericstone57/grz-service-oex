"""
ASGI config for asics_wxa project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path
import environ

from django.core.asgi import get_asgi_application
from django.core.exceptions import ImproperlyConfigured
from starlette.middleware.cors import CORSMiddleware

env = environ.Env()

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "grz_service_oex"))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

django_application = get_asgi_application()

# Import websocket application here, so apps from django_application are loaded first
from config.websocket import websocket_application  # noqa isort:skip


async def application(scope, receive, send):
    if scope["type"] == "http":
        await django_application(scope, receive, send)
    elif scope["type"] == "websocket":
        await websocket_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")


from fastapi import FastAPI
from fast_api.api.v1.api import api_router

fastapp = FastAPI(
    openapi_url='/api/v1/oex/openapi.json',
    docs_url='/api/v1/oex/docs'
)
fastapp.include_router(api_router, prefix='/api/v1/oex')

try:
    fastapp.add_middleware(
        CORSMiddleware,
        allow_origins=env.list('BACKEND_CORS_ORIGINS'),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
except ImproperlyConfigured:
    pass