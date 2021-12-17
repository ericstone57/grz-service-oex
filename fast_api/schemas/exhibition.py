from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from fast_api.schemas.space import SpaceSimpleORM, SpaceSimpleOut


class WorkSimpleORM(BaseModel):
    id: str
    title: str
    cover: str = Field(alias='cover_link', default='')
    price: float = None
    status: str
    status_text: str

    class Config:
        orm_mode = True


class ExhibitionSimpleORM(BaseModel):
    id: str
    title: str
    cover_s: str = Field(alias='cover_s_link', default='')
    start_at: datetime = Field(alias='start_at_local', default='')
    end_at: datetime = Field(alias='end_at_local', default='')
    fav_cnt: int = Field(alias='favorite_count', default='')
    days_left: int = 0

    class Config:
        orm_mode = True


class ExhibitionORM(BaseModel):
    id: str
    title: str
    cover: str = Field(alias='cover_link', default='')
    start_at: datetime = Field(alias='start_at_local', default='')
    end_at: datetime = Field(alias='end_at_local', default='')
    fav_cnt: int = Field(alias='favorite_count', default='')
    days_left: int = 0
    intro: str = ''
    curator: str = ''
    author: str = ''
    space: SpaceSimpleORM = None
    works: List[WorkSimpleORM] = []

    class Config:
        orm_mode = True


class WorkORM(BaseModel):
    id: str
    title: str
    cover: str = Field(alias='cover_link', default='')
    price: float = None
    status: str = None
    status_text: str = None
    intro: str = None
    size: str = None
    copyright: str = None
    inventory: int = None
    exhibition: ExhibitionSimpleORM = None

    class Config:
        orm_mode = True


class WorkSimpleOut(BaseModel):
    id: str
    title: str = ''
    cover: str = ''
    price: float = None
    status: str = ''
    status_text: str = ''


class ExhibitionOut(BaseModel):
    id: str
    title: str = ''
    cover: str = ''
    start_at: datetime = ''
    end_at: datetime = ''
    fav_cnt: int = 0
    days_left: int = 0
    days_left_text_format: str = '离结束还有：{}天'
    intro: str = ''
    curator: str = ''
    author: str = ''
    space: SpaceSimpleOut = None
    works: List[WorkSimpleOut] = []


class ExhibitionSimpleOut(BaseModel):
    id: str
    title: str = ''
    cover_s: str = ''
    start_at: datetime = ''
    end_at: datetime = ''
    fav_cnt: int = 0
    days_left: int = 0
    days_left_text_format: str = '离结束还有：{}天'


class WorkOut(BaseModel):
    id: str
    title: str = ''
    cover: str = ''
    price: float = None
    status: str = ''
    status_text: str = ''
    intro: str = ''
    size: str = ''
    copyright: str = ''
    inventory: int = 0
    exhibition: ExhibitionSimpleOut = None


class ExhibitionsOut(BaseModel):
    count: int = 0
    data: List[ExhibitionSimpleOut] = []

    @classmethod
    def fill(cls, data: List[ExhibitionSimpleORM] = []):
        return cls(
            count=len(data),
            data=data
        )
