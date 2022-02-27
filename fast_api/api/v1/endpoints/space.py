import logging
from enum import Enum
from typing import List

import environ
from fastapi import APIRouter, Depends, File, UploadFile
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from fast_api.adapters.space import retrieve_all, retrieve_one, create, save_pic
from fast_api.schemas.space import SpaceSimpleORM, SpacesOut, SpaceOut, SpaceORM, SpaceCreateIn

env = environ.Env()
router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/', response_model=SpacesOut)
def get_all(spaces: List[SpaceSimpleORM] = Depends(retrieve_all)):
    return SpacesOut.fill(data=spaces)


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
