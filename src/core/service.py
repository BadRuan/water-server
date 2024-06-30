from copy import deepcopy
from typing import List
from core.model import Station
from core.settings import STATIONS
from core.dao import table1_waterlevel, table2_waterlevel, table3_waterlevel


def func(stations: List[Station], waterline_colum):
    for station in stations:  # 遍历每个测站
        for cow in waterline_colum:  # 每列数据
            if station.stcd == cow.stcd:
                station.waterline.append(cow.current)


async def get_waterlevel_1() -> List[Station]:
    stations = deepcopy(STATIONS)
    for d in await table1_waterlevel():
        func(stations, d)
    return stations


async def get_waterlevel_2() -> List[Station]:
    stations = deepcopy(STATIONS)
    for d in await table2_waterlevel():
        func(stations, d)
    return stations


async def get_waterlevel_3() -> List[Station]:
    stations = deepcopy(STATIONS)
    for d in await table3_waterlevel():
        func(stations, d)
    return stations
