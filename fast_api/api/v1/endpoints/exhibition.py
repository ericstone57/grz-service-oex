import logging
from typing import List

import environ
from fastapi import APIRouter, Depends

from fast_api.adapters.exhibition import retrieve_all, retrieve_by_space, retrieve_ended_by_space, retrieve_one, \
    retrieve_work
from fast_api.schemas.exhibition import ExhibitionSimpleORM, ExhibitionsOut, ExhibitionOut, ExhibitionORM, WorkORM, \
    WorkOut, ExhibitionForStorekeeperSimpleOut
from grz_service_oex.oex.models import Exhibition

env = environ.Env()
router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/', response_model=ExhibitionsOut)
def get_all(exhibitions: List[ExhibitionSimpleORM] = Depends(retrieve_all)):
    return ExhibitionsOut.fill(data=exhibitions)


@router.get('/{id}/', response_model=ExhibitionOut)
def get_one(exhibition: ExhibitionORM = Depends(retrieve_one)):
    return ExhibitionOut(**exhibition.dict())


@router.get('/by_space/{space_id}/', response_model=ExhibitionsOut)
def get_by_space(exhibitions: List[ExhibitionSimpleORM] = Depends(retrieve_by_space)):
    return ExhibitionsOut.fill(data=exhibitions)


@router.get('/by_space/{space_id}/ended/', response_model=ExhibitionsOut)
def get_by_space(exhibitions: List[ExhibitionSimpleORM] = Depends(retrieve_ended_by_space)):
    return ExhibitionsOut.fill(data=exhibitions)


@router.get('/work/{id}/', response_model=WorkOut)
def get_one(work: WorkORM = Depends(retrieve_work)):
    return WorkOut(**work.dict())


@router.get('/storekeeper/by_space/{space_id}/')
def get_by_space_as_storekeeper(space_id: str):
    return [ExhibitionForStorekeeperSimpleOut(**ExhibitionSimpleORM.from_orm(o).dict()) for o in Exhibition.retrieve_by_space_as_storekeeper(space_id=space_id)]
