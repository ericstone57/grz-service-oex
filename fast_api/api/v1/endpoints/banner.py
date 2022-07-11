import logging
from typing import List

import environ
from fastapi import APIRouter, Depends

from fast_api.adapters.banner import retrieve_all, retrieve_owner_all
from fast_api.schemas.banner import BannerModel, BannersOut

env = environ.Env()
router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/', response_model=BannersOut)
def get_all(banners: List[BannerModel] = Depends(retrieve_all)):
    return BannersOut.fill(data=banners)


@router.get('/storekeeper/', response_model=BannersOut)
def get_all(banners: List[BannerModel] = Depends(retrieve_owner_all)):
    return BannersOut.fill(data=banners)
