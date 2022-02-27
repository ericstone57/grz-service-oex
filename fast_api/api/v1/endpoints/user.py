import logging

import httpx
from fastapi import APIRouter, HTTPException

from fast_api.adapters.user import save_login, save_info, fetch_one
from fast_api.schemas.user import UserLoginIn, UserOut, UserInfoIn

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/login/', response_model=UserOut)
async def login(post: UserLoginIn):
    # resp = httpx.post("https://s.e0x233.com/api/v1/social/wxmp/W5hJJ3dheck9/login/", json=post.dict())
    resp = httpx.post("http://127.0.0.1:8012/api/v1/social/wxmp/W5hJJ3dheck9/login/", json=post.dict())
    if resp.status_code == 200:
        user = await save_login(resp.json())
        return user.dict()

    logger.error(resp.text)
    raise HTTPException(status_code=400, detail=str(resp.text))


@router.post('/info/', response_model=UserOut)
async def update_info(post: UserInfoIn):
    resp = httpx.post("http://127.0.0.1:8012/api/v1/social/wxmp/W5hJJ3dheck9/decode/user/", json=post.dict())
    if resp.status_code == 200:
        user = await save_info({'uid': post.uid, **resp.json()})
        return user.dict()

    logger.error(resp.text)
    raise HTTPException(status_code=400, detail=str(resp.text))


@router.get('/{uid}/', response_model=UserOut)
async def user(uid: str):
    try:
        user = await fetch_one(uid)
        return user.dict()
    except Exception:
        raise HTTPException(status_code=404, detail='user not exist')
