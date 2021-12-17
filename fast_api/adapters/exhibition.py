from typing import List

from fast_api.schemas.exhibition import ExhibitionSimpleORM, ExhibitionORM, WorkORM
from grz_service_oex.oex.models import Exhibition, Work
from ks_shared.fastapi.adapters import retrieve_object


def retrieve_all() -> List[ExhibitionSimpleORM]:
    return [ExhibitionSimpleORM.from_orm(o) for o in Exhibition.retrieve_all()]


def retrieve_one(id: str) -> ExhibitionORM:
    return ExhibitionORM.from_orm(retrieve_object(Exhibition, id=id))


def retrieve_by_space(space_id: str) -> List[ExhibitionSimpleORM]:
    return [ExhibitionSimpleORM.from_orm(o) for o in Exhibition.retrieve_by_space(space_id=space_id)]


def retrieve_ended_by_space(space_id: str) -> List[ExhibitionSimpleORM]:
    return [ExhibitionSimpleORM.from_orm(o) for o in Exhibition.retrieve_by_space(space_id=space_id, is_end=True)]


def retrieve_work(id: str) -> ExhibitionORM:
    return WorkORM.from_orm(retrieve_object(Work, id=id))
