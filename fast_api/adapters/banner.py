import logging
from typing import List

from asgiref.sync import sync_to_async, async_to_sync
from fastapi import Path
from ks_shared.fastapi.adapters import retrieve_object

from fast_api.schemas.banner import BannerModel
from grz_service_oex.oex.models import Banner


def retrieve_banner(
        id: int = Path(..., description="get banner from db")
) -> Banner:
    return retrieve_object(Banner, id)


# @sync_to_async()
# def banner_retrieve_all():
#     return list(Banner.retrieve_all())

# async def retrieve_all() -> List[Banner]:
#     return await banner_retrieve_all()

def retrieve_all() -> List[BannerModel]:
    return [BannerModel.from_orm(o) for o in Banner.retrieve_all()]
