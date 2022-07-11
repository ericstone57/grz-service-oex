import logging
from typing import List

import environ
from enum import Enum
from fastapi import APIRouter, Depends, File, UploadFile
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from fast_api.adapters.space import retrieve_all, retrieve_one, create, save_pic, retrieve_by_user
from fast_api.schemas.space import SpaceSimpleORM, SpaceOut, SpaceORM, SpaceCreateIn, SpaceSimpleOut

env = environ.Env()
router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/', response_model=List[SpaceSimpleOut],
            description="""
**st_geo**, search through geolocation

**user_geo**, user geolocation, used to calculate distance to destination

use 116.481028,39.989643 format as parameter for geolocation
            """)
def get_all(spaces: List[SpaceSimpleORM] = Depends(retrieve_all)):
    return [SpaceSimpleOut(**o.dict()) for o in spaces]


@router.get('/{space_id}/', response_model=SpaceOut)
def get_one(space: SpaceORM = Depends(retrieve_one)):
    return SpaceOut(**space.dict())


@router.post('/', response_model=SpaceOut)
async def create_space(post: SpaceCreateIn):
    return await create(post)


class PicCategory(str, Enum):
    outside = 'outside'
    inside = 'inside'
    other = 'other'


@router.post('/{space_id}/pic/{category}/')
async def upload_pic(
    space_id: str,
    category: PicCategory,
    file: UploadFile = File(...),
):
    await save_pic(space_id, category, file)
    return Response(status_code=HTTP_200_OK)


@router.get('/by_user/{user_id}/')
def get_by_user(user_id: str):
    return [SpaceSimpleOut(**o.dict()) for o in retrieve_by_user(user_id)]
