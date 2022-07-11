from typing import List

from fastapi import Path
from ks_shared.fastapi.adapters import retrieve_object

from fast_api.schemas.banner import BannerModel
from grz_service_oex.oex.models import Banner


def retrieve_banner(
        id: int = Path(..., description="get banner from db")
) -> Banner:
    return retrieve_object(Banner, id)


def retrieve_all() -> List[BannerModel]:
    return [BannerModel.from_orm(o) for o in Banner.retrieve_all()]


def retrieve_owner_all() -> List[BannerModel]:
    return [BannerModel.from_orm(o) for o in Banner.retrieve_all(belong_to='storekeeper')]
