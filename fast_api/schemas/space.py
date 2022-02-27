from datetime import time
from typing import List, Optional

from pydantic import BaseModel, Field


class SpaceORM(BaseModel):
    id: str
    title: str
    cover: str = Field(alias='cover_link', default='')
    cover_s: str = Field(alias='cover_s_link', default='')
    address: str
    province: str
    city: str
    longitude: float = None
    latitude: float = None
    intro: str
    opentime_from: Optional[time]
    opentime_to: Optional[time]
    tags: List[dict] = Field(alias='tags_all', default='')
    fav_cnt: int = Field(alias='favorite_count', default='')
    work_spaces: List[dict]

    class Config:
        orm_mode = True


class SpaceSimpleORM(BaseModel):
    id: str
    title: str
    cover_s: str = Field(alias='cover_s_link', default='')
    address: str
    tags: List[dict] = Field(alias='tags_all', default='')
    fav_cnt: int = Field(alias='favorite_count', default='')

    class Config:
        orm_mode = True


class SpaceOut(BaseModel):
    id: str
    title: str
    cover: str = ''
    cover_s: str = ''
    address: str = ''
    province: str = ''
    city: str = ''
    longitude: float = None
    latitude: float = None
    intro: str = ''
    opentime_from: Optional[time] = None
    opentime_to: Optional[time] = None
    tags: List[dict] = []
    fav_cnt: int = 0
    work_spaces: List[dict] = []

    class Config:
        json_encoders = {
            time: lambda t: t.strftime('%H:%M')
        }


class SpaceSimpleOut(BaseModel):
    id: str
    title: str
    cover_s: str = ''
    address: str = ''
    distance: int = 2000
    tags: List[dict] = []
    fav_cnt: int = 0


class SpacesOut(BaseModel):
    count: int = 0
    data: List[SpaceSimpleOut] = []

    @classmethod
    def fill(cls, data: List[SpaceSimpleORM] = []):
        return cls(
            count=len(data),
            data=data
        )


class SpaceCreateIn(BaseModel):
    uid: str
    title: str
    province: str
    city: str
    district: str
    address: str
    space_area: str
    contact_cellphone: str
    # outside_pics: List[str]
    # inside_pics: List[str]
    # other_pics: List[str]

