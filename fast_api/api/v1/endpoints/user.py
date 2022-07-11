import logging
import environ

import httpx
from fastapi import APIRouter, HTTPException, status
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from fast_api.adapters.user import save_login, save_info, fetch_one, fetch_storekeeper_status, update_phone
from fast_api.schemas.user import UserLoginIn, UserOut, UserInfoIn, PhoneIn

logger = logging.getLogger(__name__)

router = APIRouter()
env = environ.Env()


@router.post('/login/', response_model=UserOut)
async def login(post: UserLoginIn):
    resp = httpx.post(f'{env("KS_SOCIAL_ENDPOINT")}/wxmp/{env("KS_ASICS_WXA_APPID")}/login/', json=post.dict())
    if resp.status_code == 200:
        user = await save_login(resp.json())
        return user.dict()

    logger.error(resp.text)
    raise HTTPException(status_code=400, detail=str(resp.text))


@router.post('/info/', response_model=UserOut)
async def update_info(post: UserInfoIn):
    resp = httpx.post(f'{env("KS_SOCIAL_ENDPOINT")}/wxmp/{env("KS_ASICS_WXA_APPID")}/decode/user/', json=post.dict())
    if resp.status_code == 200:
        user = await save_info({'uid': post.uid, **resp.json()})
        return user.dict()

    logger.error(resp.text)
    raise HTTPException(status_code=400, detail=str(resp.text))


@router.post('/phone/')
async def phone(post: PhoneIn):
    if post.code:
        resp = httpx.post(f'{env("KS_SOCIAL_ENDPOINT")}/wxmp/{env("KS_ASICS_WXA_APPID")}/phone_number/', json=post.dict())
    else:
        resp = httpx.post(f'{env("KS_SOCIAL_ENDPOINT")}/wxmp/{env("KS_ASICS_WXA_APPID")}/decode/phone2/', json=post.dict())

    if resp.status_code == status.HTTP_200_OK:
        await update_phone({'uid': post.uid, **resp.json()})
        return Response(status_code=HTTP_200_OK)

    raise HTTPException(status_code=404, detail=resp.json()['detail'])


@router.get('/{uid}/', response_model=UserOut)
async def user(uid: str):
    try:
        user = await fetch_one(uid)
        return user.dict()
    except Exception:
        raise HTTPException(status_code=404, detail='user not exist')


@router.get('/{uid}/storekeeper_status/')
async def user(uid: str) -> str:
    try:
        return await fetch_storekeeper_status(uid)
    except Exception:
        raise HTTPException(status_code=404, detail='user not exist')