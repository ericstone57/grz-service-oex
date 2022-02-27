from typing import List
from asgiref.sync import sync_to_async

from fast_api.schemas.space import SpaceSimpleORM, SpaceORM, SpaceCreateIn
from grz_service_oex.oex.models import Space, SpacePicture
from ks_shared.fastapi.adapters import retrieve_object
from ks_shared.django.model_utils import load_image_from_url
from django.core.files.uploadedfile import InMemoryUploadedFile
from fastapi import UploadFile


def retrieve_all() -> List[SpaceSimpleORM]:
    return [SpaceSimpleORM.from_orm(o) for o in Space.retrieve_all()]


def retrieve_one(space_id: str) -> SpaceORM:
    return SpaceORM.from_orm(retrieve_object(Space, id=space_id))


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
    p.file = InMemoryUploadedFile(file.file, 'file', file.filename, file.content_type, None, None)
    p.save()


async def save_pic(space_id: str, category: str, file: UploadFile):
    return await sync_to_async(_upload_pic, thread_sensitive=True)(space_id, category, file)

