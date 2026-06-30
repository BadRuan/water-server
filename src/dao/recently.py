from typing import List, NamedTuple
from datetime import timedelta, datetime
import asyncio
from src.utils import get_logger, fetch_row_one
from src.model import WaterItem
from src.settings import station_list, Station


log = get_logger(__name__)


class RecentlyBaseStation(NamedTuple):
    code: int
    name: str
    water_item: WaterItem


async def _fetch_station_recent(station: Station) -> RecentlyBaseStation | None:
    """查询单个站点的最新水位及昨日同期水位。"""
    # 获取最新记录
    sql = f"SELECT * FROM station_{station.code} ORDER BY ts DESC LIMIT 1"
    result = await fetch_row_one(sql)
    if result is None:
        return None

    # 获取昨日同期数据
    target_time: datetime = (result[0] - timedelta(days=1)).replace(minute=0, second=0)
    sql_yesterday = f"SELECT * FROM station_{station.code} WHERE ts = date_trunc('second', $1::timestamp)"
    yesterday = await fetch_row_one(sql_yesterday, target_time)
    if yesterday is None:
        return None

    water_item = WaterItem(
        height=result[1],
        yesterday_height=yesterday[1],
        timestamp=result[0],
        code=station.code,
    )
    return RecentlyBaseStation(code=station.code, name=station.name, water_item=water_item)


async def get_recently_data() -> List[RecentlyBaseStation]:
    """并发查询所有站点的最新水位数据。"""
    tasks = [_fetch_station_recent(station) for station in station_list]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    recently_data: List[RecentlyBaseStation] = []
    for result in results:
        if isinstance(result, Exception):
            log.error(f"查询站点数据失败: {result}")
        elif result is not None:
            recently_data.append(result) # type: ignore
    return recently_data
