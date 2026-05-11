from typing import List, NamedTuple
from src.utils import Storage, Logger
from src.model import WaterItem
from src.settings import station_list


log = Logger(__name__)


class RecentlyBaseStation(NamedTuple):
    code: int 
    name: str
    water_item: WaterItem
 
def get_recently_data() -> List[RecentlyBaseStation]:
    recently_data: List[RecentlyBaseStation] = []
    with Storage() as storage:
        for base_station in station_list:
            sql: str = f"select *  from station_{base_station.code} where ts = (SELECT MAX(ts) FROM station_{base_station.code});"
            result = storage.query_one(sql)
            if result is not None:
                water_item_tmp = WaterItem(height=result[1],timestamp=result[0], code=base_station.code)
                recently_data.append(RecentlyBaseStation(code=base_station.code, name=base_station.name, water_item=water_item_tmp))
        return recently_data
    