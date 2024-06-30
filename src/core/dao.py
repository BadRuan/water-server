from typing import List
from copy import deepcopy
from datetime import datetime, timedelta
from core.model import WaterLevel, Station
from core.settings import STATIONS
from util.tdenginetool import TDengineTool


# 查询指定日期时间的整点水位
async def select_waterlevel(date: datetime) -> List[WaterLevel]:
    sql = f"""SELECT `ts`, `current`, `stcd`, `name` FROM waterlevel WHERE `ts`='{date.strftime("%Y-%m-%d %H")}:00:00' """
    with TDengineTool() as td:
        result = td.query(sql)
        return [
            WaterLevel(
                tm=row[0][:-7],
                current=round(row[1], 2),  # 水位数据保留小数点后2位
                stcd=row[2],
                name=row[3],
            )
            for row in result
        ]


def func(stations: List[Station], waterline_colum):
    for station in stations:  # 遍历每个测站
        for cow in waterline_colum:  # 每列数据
            if station.stcd == cow.stcd:
                station.waterline.append(cow.current)


# 获取表1数据
async def table1_data() -> List[Station]:
    stations: List[Station] = deepcopy(STATIONS)

    today = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    func(stations, await select_waterlevel(today))
    func(stations, await select_waterlevel(today - timedelta(days=1)))
    func(stations, await select_waterlevel(today - timedelta(weeks=1)))
    func(stations, await select_waterlevel(today.replace(year=today.year - 1)))

    return stations


# 获取表2数据
async def table2_data() -> List[Station]:
    stations = deepcopy(STATIONS)

    date_now = datetime.now()
    func(stations, await select_waterlevel(date_now))
    func(stations, await select_waterlevel(date_now - timedelta(days=1)))

    return stations


# 获取表3数据
async def table3_data() -> List[Station]:
    stations = deepcopy(STATIONS)

    date_now = datetime.now()
    func(stations, await select_waterlevel(date_now))
    func(stations, await select_waterlevel(date_now - timedelta(hours=2)))
    func(stations, await select_waterlevel(date_now - timedelta(hours=4)))
    func(stations, await select_waterlevel(date_now - timedelta(hours=6)))
    func(stations, await select_waterlevel(date_now - timedelta(hours=8)))
    func(stations, await select_waterlevel(date_now - timedelta(hours=10)))

    return stations
