# -*- coding: utf-8 -*-

from typing import List, Dict, Optional
from ..model.enums import CommonStatus, StreamSpiderGroupType
from ..model.entity import StreamSpiderGroup, StreamSpider
from ..dao import stream_spider_group as stream_spider_group_dao


def get_all_stream_spider_groups() -> List[Dict[str, str]]:
    """
    获取所有的爬虫组
    """

    return StreamSpiderGroupType.to_list()


def get_spiders_by_group(group_code: str, status: str = CommonStatus.ON.name) -> List[StreamSpiderGroup]:
    """
    根据一个爬虫组编码，获取里面所有的爬虫
    """
    rows = stream_spider_group_dao.get_spider_group_list(group_code=group_code, status=status)
    rows = [StreamSpiderGroup(**x) for x in rows]

    return rows


def get_spider(spider_id: str, status: str = CommonStatus.ON.name) -> Optional[StreamSpider]:
    """
    获取爬虫详情
    """

    stream_spider = stream_spider_group_dao.get_spider_by_spider_id(spider_id=spider_id, status=status)

    return stream_spider

