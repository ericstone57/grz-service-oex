import logging

import environ
from fastapi import APIRouter

from fast_api.schemas.msg import MessageORM, MessageThreadORM
from grz_service_oex.oex.models import MessageThread

env = environ.Env()
router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/user/{user_id}/')
def get_msg_threads(user_id: str):
    return [MessageThreadORM.fill(o) for o in MessageThread.retrieve_by_receiver(user_id)]


@router.get('/user/{user_id}/thread/{thread_id}/')
def get_msg_thread_detail(user_id: str, thread_id: str):
    o = MessageThread.objects.get(id=thread_id)
    return MessageThreadORM.fill(o)


@router.get('/user/{user_id}/thread/{thread_id}/dialog/')
def get_dialog(user_id: str, thread_id: str):
    return [MessageORM.fill(o) for o in MessageThread.objects.filter(id=thread_id, receiver_id=user_id).first().conversation()]


@router.post('/user/{user_id}/thread/{thread_id}/read/')
def make_read(user_id: str, thread_id: str):
    MessageThread.objects.get(id=thread_id, receiver_id=user_id).make_read()
    return 'ok'
