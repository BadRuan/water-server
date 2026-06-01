from typing import List, NamedTuple
from datetime import timedelta, datetime
from src.utils import Logger, fetch_row_one
from src.model import WaterItem
from src.settings import station_list


log = Logger(__name__)

class RecentlyBaseStation(NamedTuple):
    code: int 
    name: str
    water_item: WaterItem
 
async def get_recently_data() -> List[RecentlyBaseStation]:
    recently_data: List[RecentlyBaseStation] = []
    for base_station in station_list:
        sql: str = f"select *  from station_{base_station.code} where ts = (SELECT MAX(ts) FROM station_{base_station.code});"
        result = await fetch_row_one(sql)               
        if result is not None:
            target_time: datetime = result[0] - timedelta(days=1)
            target_time = target_time.replace(minute=0,second=0)
            sql_for_yesterday: str = f"select * from station_{base_station.code} where ts = '{target_time}';"
            yesterday = await fetch_row_one(sql_for_yesterday)
            if yesterday is not None:
                water_item_tmp = WaterItem(height=result[1], yesterday_height=yesterday[1],timestamp=result[0], code=base_station.code)
                recently_data.append(RecentlyBaseStation(code=base_station.code, name=base_station.name, water_item=water_item_tmp))
    return recently_data
    