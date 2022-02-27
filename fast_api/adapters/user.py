from asgiref.sync import sync_to_async

from fast_api.schemas.user import UserMode, StorekeeperMode
from grz_service_oex.oex.models import Space
from grz_service_oex.user.models import User


def _login(data: dict):
    return UserMode.from_orm(User.login(data))


async def save_login(data: dict):
    return await sync_to_async(_login, thread_sensitive=True)(data)


def _save_info(data: dict):
    return UserMode.from_orm(User.update_info(data))


async def save_info(data: dict):
    return await sync_to_async(_save_info, thread_sensitive=True)(data)


def _fetch_one(uid: str):
    return UserMode.from_orm(User.objects.get(id=uid))


async def fetch_one(uid: str):
    return await sync_to_async(_fetch_one, thread_sensitive=True)(uid)


def _fetch_storekeeper_status(uid: str):
    return Space.retrieve_storekeeper_status(user_id=uid)


async def fetch_storekeeper_status(uid: str):
    return await sync_to_async(_fetch_storekeeper_status, thread_sensitive=True)(uid)
