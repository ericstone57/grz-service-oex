from datetime import datetime
from typing import Any

from pydantic.main import BaseModel

from fast_api.schemas.exhibition import ExhibitionSimplestORM
from fast_api.schemas.space import SpaceSimplestORM
from fast_api.schemas.user import UserSimpleMode
from grz_service_oex.oex.models import Space, Exhibition


class MessageSimpleORM(BaseModel):
    id: str
    title: str
    content: str
    created: datetime

    class Config:
        orm_mode = True


class MessageORM(BaseModel):
    id: str
    title: str
    content: str
    created: datetime
    msg_type: str
    is_read: bool = False
    object_type: str
    object: Any = None

    class Config:
        orm_mode = True

    @classmethod
    def fill(cls, obj):
        model = cls.from_orm(obj)
        if obj.object_type == 'space':
            model.object = SpaceSimplestORM.from_orm(Space.objects.get(id=obj.object_id))
        if obj.object_type == 'exhibition':
            model.object = ExhibitionSimplestORM.from_orm(Exhibition.objects.get(id=obj.object_id))
        return model


class MessageThreadORM(BaseModel):
    id: str
    sender: UserSimpleMode
    receiver: UserSimpleMode
    type: str
    is_read: bool = False
    object_type: str
    object: Any = None
    latest_msg_at: datetime
    latest_msg: MessageSimpleORM = None

    class Config:
        orm_mode = True

    @classmethod
    def fill(cls, obj):
        model = cls.from_orm(obj)
        model.latest_msg = MessageSimpleORM.from_orm(obj.messages.last())
        # if obj.object_type == 'space':
        #     model.object = SpaceSimplestORM.from_orm(Space.objects.get(id=obj.object_id))
        # if obj.object_type == 'exhibition':
        #     model.object = ExhibitionSimplestORM.from_orm(Exhibition.objects.get(id=obj.object_id))
        return model


