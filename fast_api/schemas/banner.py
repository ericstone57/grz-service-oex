from typing import List

from pydantic import BaseModel, Field, root_validator


class LinkModel(BaseModel):
    name: str
    url: str = ''
    type: str = Field(alias='type_code', default='')
    wxmp_appid: str = ''
    wxmp_pagepath: str = ''

    class Config:
        orm_mode = True


class LinkOut(BaseModel):
    name: str
    url: str = ''
    type: str = ''
    wxmp_appid: str = ''
    wxmp_pagepath: str = ''


class BannerModel(BaseModel):
    id: str
    name: str
    link: LinkModel = None
    pic: str = Field(alias='pic_link', default='')

    @root_validator()
    def convert_filed_name(cls, values):
        if 'link' in values and values['link']:
            values['link'] = LinkOut(**values['link'].dict())
        return values

    class Config:
        orm_mode = True


class BannerOut(BaseModel):
    id: str
    name: str
    link: dict = None
    pic: str = ''


class BannersOut(BaseModel):
    count: int = 0
    data: List[BannerOut] = []

    @classmethod
    def fill(cls, data: List[BannerModel] = []):
        return cls(
            count=len(data),
            data=data
        )
