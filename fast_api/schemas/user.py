from pydantic import BaseModel, Field


class UserLoginIn(BaseModel):
    code: str
    utm_source: str = ''


class UserInfoIn(BaseModel):
    uid: str
    encryptedData: str
    iv: str


class UserOut(BaseModel):
    id: str
    openid: str
    unionid: str = ''
    name: str = ''
    gender: str = ''
    avatar: str = ''
    seed: str = ''
    is_info_fulfill: bool = False
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
    role: str

    class Config:
        orm_mode = True

