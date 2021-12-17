import logging

from asgiref.sync import sync_to_async
from fastapi import HTTPException, Body

from grz_service_oex.oex.models import Config
from grz_service_oex.user.models import Config as UserConfig

logger = logging.getLogger(__name__)


async def retrieve_oex_config(key: str = Body(..., embed=True)):
    try:
        return await sync_to_async(Config.objects.get, thread_sensitive=True)(key=key)
    except Config.DoesNotExist:
        msg = f"{key} is invalid key."
        raise HTTPException(status_code=400, detail=msg)


async def retrieve_user_config(key: str = Body(..., embed=True)):
    try:
        return await sync_to_async(UserConfig.objects.get, thread_sensitive=True)(key=key)
    except UserConfig.DoesNotExist:
        msg = f"{key} is invalid key."
        raise HTTPException(status_code=400, detail=msg)
