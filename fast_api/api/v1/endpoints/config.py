import logging

import environ
from fastapi import APIRouter, Depends

from fast_api.adapters.config import retrieve_user_config
from grz_service_oex.user.models import Config

env = environ.Env()
router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/init/')
async def init(config: Config = Depends(retrieve_user_config)):
    return config.value
