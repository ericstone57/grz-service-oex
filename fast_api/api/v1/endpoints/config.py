import logging

import environ
from fastapi import APIRouter, Depends

from fast_api.adapters.config import retrieve_user_config, retrieve_oex_config
from grz_service_oex.oex.models import Config
from grz_service_oex.user.models import Config as UserConfig

env = environ.Env()
router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/init/')
async def init(config: Config = Depends(retrieve_oex_config)):
    return config.value


@router.post('/init/user/')
async def init(config: UserConfig = Depends(retrieve_user_config)):
    return config.value
