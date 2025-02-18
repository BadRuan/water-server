from typing import List
from datetime import datetime, timedelta
from model import Station
from utils.logger import Logger
from dao.base_dao import TableDao

logger = Logger(__name__)


# 获取表1数据
class Table1_Dao(TableDao):

    def __init__(self) -> None:
        super().__init__()

    def get_table_data(self) -> List[Station]:
        target = [
            datetime.now().replace(hour=8),  # 今日 8:00
            datetime.now().replace(hour=8) - timedelta(days=1),  # 昨日 8:00
            datetime.now().replace(hour=8) - timedelta(weeks=1),  # 上周 8:00
            datetime.now().replace(hour=8) - timedelta(days=365),  # 去年今日 8:00
        ]

        return self.fetch_station_data(target)


# 获取表2数据
class Table2_Dao(TableDao):

    def __init__(self) -> None:
        super().__init__()

    def get_table_data(self) -> List[Station]:
        target = [
            datetime.now(),  # 当前时刻
            datetime.now() - timedelta(hours=4),  # 四小时前
            datetime.now() - timedelta(hours=8),  # 八小时前
        ]

        return self.fetch_station_data(target)
