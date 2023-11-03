# encoding: utf-8

from typing import Optional
from zcbot_crawl_core.client.mongo_client import Mongo
from zcbot_crawl_core.model.enums import CommonStatus
from zcbot_crawl_core.model.entity import StreamSpider


def get_spider_group_list(group_code: str, status: str = CommonStatus.ON.name):
    _query = {}
    if group_code:
        _query['groupCode'] = group_code

    _query['status'] = status

    return Mongo().list(collection="zcbot_stream_spider_group", query=_query)


def get_spider_by_spider_id(spider_id: str, status: str = CommonStatus.ON.name) -> Optional[StreamSpider]:
    _query = {
        "_id": spider_id,
        "status": status
    }
    result = Mongo().get(collection="zcbot_stream_spider", query=_query)

    if result:
        return StreamSpider(**result)

    return None
