from abc import abstractmethod
from typing import List
from copy import deepcopy
from datetime import datetime, timedelta
from core.model import WaterLevel, Station
from core.settings import STATIONS
from util.tdenginetool import TDengineTool
from util.othertool import today_or_yesterday


class TableDao:

    def __init__(self) -> None:
        self.stations = deepcopy(STATIONS)

    # 将水位数据添加到对应的测站中
    def _add_waterdata_to_stations(
        self, stations: List[Station], waterlevels: List[WaterLevel]
    ):
        # 创建一个字典，键为站点代码，值为当前水位
        waterlevel_map = {wl.stcd: wl.current for wl in waterlevels}
        for station in stations:
            # 从字典中查找对应站点的水位，若不存在则添加0
            station.waterline.append(waterlevel_map.get(station.stcd, 0))

    # 通用的数据获取函数，用于获取不同时间点的水位数据
    async def fetch_station_data(self, time_points: List[datetime]) -> List[Station]:
        # 对于每个时间点，查询并添加水位数据
        for time_point in time_points:
            waterlevels = await self.select_waterlevel(time_point)
            self._add_waterdata_to_stations(self.stations, waterlevels)
        return self.stations

    # 异步查询指定日期时间的整点水位
    async def select_waterlevel(self, date: datetime) -> List[WaterLevel]:
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

    @abstractmethod
    async def get_table_data(self) -> List[Station]:
        pass


# 获取表1数据
class Table1_Dao(TableDao):

    def __init__(self) -> None:
        super().__init__()

    async def get_table_data(self) -> List[Station]:
        return await self.fetch_station_data(
            [
                datetime.now().replace(hour=8),  # 当前日期8点整
                datetime.now().replace(hour=8) - timedelta(days=1),  # 昨天8点整
                datetime.now().replace(hour=8) - timedelta(weeks=1),  # 一周前8点整
                datetime.now()
                .replace(hour=8)
                .replace(year=datetime.now().year - 1),  # 去年同期8点整
            ]
        )


# 获取表2数据
class Table2_Dao(TableDao):

    def __init__(self) -> None:
        super().__init__()

    async def get_table_data(self) -> List[Station]:
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
        return await self.fetch_station_data(target)


# 获取表3数据
class Table3_Dao(TableDao):

    def __init__(self) -> None:
        super().__init__()

    async def get_table_data(self) -> List[Station]:
        target = [
            datetime.now(),  # 当前时刻
            datetime.now() - timedelta(hours=4),  # 四小时前
        ]
        target.append(
            today_or_yesterday(
                datetime.now().replace(hour=8),
                datetime.now().replace(hour=8) - timedelta(days=1),
            )
        )
        return await self.fetch_station_data(target)

