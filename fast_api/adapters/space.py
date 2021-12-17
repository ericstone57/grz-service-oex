from typing import List

from fast_api.schemas.space import SpaceSimpleORM, SpaceORM
from grz_service_oex.oex.models import Space
from ks_shared.fastapi.adapters import retrieve_object


def retrieve_all() -> List[SpaceSimpleORM]:
    return [SpaceSimpleORM.from_orm(o) for o in Space.retrieve_all()]


def retrieve_one(id: str) -> SpaceORM:
    return SpaceORM.from_orm(retrieve_object(Space, id=id))
