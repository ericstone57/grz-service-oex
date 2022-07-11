from typing import List

from asgiref.sync import sync_to_async
from django.core.files.uploadedfile import InMemoryUploadedFile
from fastapi import UploadFile
from ks_shared.fastapi.adapters import retrieve_object

from fast_api.schemas.space import SpaceSimpleORM, SpaceORM, SpaceCreateIn
from grz_service_oex.oex.models import Space, SpacePicture


def retrieve_all(st_geo=None, user_geo=None, page=1) -> List[SpaceSimpleORM]:
    """
    st_geo, search through geolocation
    user_geo, user geolocation, used to calculate distance to destination
    use 116.481028,39.989643 format as parameter for geolocation
    """
    if st_geo:
        return [SpaceSimpleORM.from_orm(o)
                for o in Space.retrieve_by_geolocation(st_geo, user_geo, page_index=page)]
    return [SpaceSimpleORM.from_orm(o) for o in Space.retrieve_all()]


def retrieve_one(space_id: str) -> SpaceORM:
    return SpaceORM.from_orm(retrieve_object(Space, id=space_id))


def retrieve_by_user(user_id: str):
    return [SpaceSimpleORM.from_orm(o) for o in Space.retrieve_all(user_id)]


def _create(data: SpaceCreateIn):
    save_data = data.dict()
    save_data['storekeeper_id'] = save_data['uid']
    del save_data['uid']
    o = Space(**save_data)
    o.save()
    return SpaceORM.from_orm(o)


async def create(data: SpaceCreateIn):
    return await sync_to_async(_create, thread_sensitive=True)(data)


def _upload_pic(space_id: str, category: str, file: UploadFile):
    p = SpacePicture()
    p.space_id = space_id
    p.category = category
    p.pic = InMemoryUploadedFile(file.file, 'file', file.filename, file.content_type, None, None)
    p.save()


async def save_pic(space_id: str, category: str, file: UploadFile):
    return await sync_to_async(_upload_pic, thread_sensitive=True)(space_id, category, file)

