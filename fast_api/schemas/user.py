from typing import Optional

from pydantic import BaseModel, Field


class UserLoginIn(BaseModel):
    code: str
    utm_source: str = ''


class UserInfoIn(BaseModel):
    uid: str
    encryptedData: str
    iv: str


class PhoneIn(BaseModel):
    uid: str
    code: Optional[str]
    encryptedData: Optional[str]
    iv: Optional[str]


class UserOut(BaseModel):
    id: str
    openid: str
    unionid: str = ''
    name: str = ''
    gender: str = ''
    avatar: str = ''
    seed: str = ''
    is_info_fulfill: bool = False
    is_phone_fulfill: bool = False
    role: str


class UserMode(BaseModel):
    id: str
    openid: str
    unionid: str = ''
    name: str = ''
    gender: str = ''
    avatar: str = Field(default='', alias='avatar_link')
    seed: str = ''
    is_info_fulfill: bool = False
    is_phone_fulfill: bool = False
    role: str

    class Config:
        orm_mode = True


class UserSimpleMode(BaseModel):
    id: str
    name: str = ''
    avatar: str = Field(default='', alias='avatar_link')

    class Config:
        orm_mode = True


class StorekeeperMode(BaseModel):
    storekeeper_status: str

    class Config:
        orm_mode = True


class StorekeeperStatus(BaseModel):
    storekeeper_status: str
