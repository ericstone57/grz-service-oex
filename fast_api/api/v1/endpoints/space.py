import logging
from typing import List

import environ
from fastapi import APIRouter, Depends

from fast_api.adapters.space import retrieve_all, retrieve_one
from fast_api.schemas.space import SpaceSimpleORM, SpacesOut, SpaceOut, SpaceORM

env = environ.Env()
router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/', response_model=SpacesOut)
def get_all(spaces: List[SpaceSimpleORM] = Depends(retrieve_all)):
    return SpacesOut.fill(data=spaces)


@router.get('/{id}/', response_model=SpaceOut)
def get_one(space: SpaceORM = Depends(retrieve_one)):
    return SpaceOut(**space.dict())
