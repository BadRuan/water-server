from typing import List
from copy import deepcopy
from datetime import datetime, timedelta
from core.model import WaterLevel, Station
from core.settings import STATIONS
from util.tdenginetool import TDengineTool
from util.othertool import today_or_yesterday


# 异步查询指定日期时间的整点水位
async def select_waterlevel(date: datetime) -> List[WaterLevel]:
    # 格式化日期时间字符串
    formatted_date = date.strftime("%Y-%m-%d %H:00:00")
    # 构造整点SQL语句
    sql = f"SELECT ts, current, stcd, name FROM waterlevel WHERE ts='{formatted_date}'"
    with TDengineTool() as td:
        results = td.query(sql)
        # 将查询结果转换为WaterLevel对象列表
        return [
            WaterLevel(
                tm=row[0].replace(":00:00", ""),  # 移除不必要的":00:00"
                current=round(row[1], 2),  # 四舍五入到两位小数
                stcd=row[2],
                name=row[3],
            )
            for row in results
        ]


# 将水位数据添加到对应的测站中
def add_waterdata_to_stations(stations: List[Station], waterlevels: List[WaterLevel]):
    # 创建一个字典，键为站点代码，值为当前水位
    waterlevel_map = {wl.stcd: wl.current for wl in waterlevels}
    for station in stations:
        # 从字典中查找对应站点的水位，若不存在则添加0
        station.waterline.append(waterlevel_map.get(station.stcd, 0))


# 通用的数据获取函数，用于获取不同时间点的水位数据
async def fetch_station_data(time_points: List[datetime]) -> List[Station]:
    stations = deepcopy(STATIONS)
    # 对于每个时间点，查询并添加水位数据
    for time_point in time_points:
        waterlevels = await select_waterlevel(time_point)
        add_waterdata_to_stations(stations, waterlevels)
    return stations


# 获取表1数据的异步函数
async def table1_data() -> List[Station]:
    return await fetch_station_data(
        [
            datetime.now().replace(hour=8),  # 当前日期8点整
            datetime.now().replace(hour=8) - timedelta(days=1),  # 昨天8点整
            datetime.now().replace(hour=8) - timedelta(weeks=1),  # 一周前8点整
            datetime.now()
            .replace(hour=8)
            .replace(year=datetime.now().year - 1),  # 去年同期8点整
        ]
    )


# 获取表2数据的异步函数
async def table2_data() -> List[Station]:
    target = [
        datetime.now(),  # 当前时刻
        datetime.now() - timedelta(hours=2),  # 两小时前
    ]
    target.append(
        today_or_yesterday(
            datetime.now().replace(hour=8),
            datetime.now().replace(hour=8) - timedelta(days=1),
        )
    )
    return await fetch_station_data(target)


# 获取表3数据的异步函数
async def table3_data() -> List[Station]:
    return await fetch_station_data(
        [
            datetime.now(),  # 当前时刻
            datetime.now() - timedelta(hours=2),  # 两小时前
            datetime.now() - timedelta(hours=4),  # 四小时前
            datetime.now() - timedelta(hours=6),  # 六小时前
            datetime.now() - timedelta(hours=8),  # 八小时前
            datetime.now() - timedelta(hours=10),  # 十小时前
        ]
    )


# 获取表4数据的异步函数
async def table4_data() -> List[Station]:
    return await fetch_station_data(
        [
            datetime.now(),  # 当前时刻
            datetime.now() - timedelta(hours=1),  # 一小时前
            datetime.now() - timedelta(hours=2),  # 两小时前
            datetime.now() - timedelta(hours=3),  # 三小时前
            datetime.now() - timedelta(hours=4),  # 四小时前
            datetime.now() - timedelta(hours=5),  # 五小时前
        ]
    )


# 水位数据总览
class StableCount:

    # 得到每个水文站点水位数据
    def all_station_count(self) -> List[tuple]:
        SQL = "SELECT name,COUNT(current) FROM waterlevel GROUP BY name"
        with TDengineTool() as td:
            result = td.query(SQL)
            return [(row[0], row[1]) for row in result]
