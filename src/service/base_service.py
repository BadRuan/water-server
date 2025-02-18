from abc import abstractmethod
from datetime import datetime, timedelta
from utils.xlsx import DataToXlsx
from dao.base_dao import TableDao


class TableService:

    def __init__(self, dao: TableDao, xlsx: DataToXlsx) -> None:
        self.dao: TableDao = dao
        self.xlsx: DataToXlsx = xlsx

    # 定义一个生成时间描述的函数
    def generate_time_description(self, hour_diff: int) -> str:
        now = datetime.now()
        target_time = now - timedelta(hours=hour_diff)
        target_date = target_time.date()
        today = now.date()
        yesterday = today - timedelta(days=1)
        if target_date == today:
            return "今日" + target_time.strftime("%H时")
        elif target_date == yesterday:
            return "昨日" + (target_time + timedelta(hours=24)).strftime("%H时")
        else:
            return target_time.strftime("%Y-%m-%d %H时")

    @abstractmethod
    def write_table_head(self):
        pass

    @abstractmethod
    async def write_data_to_table(self):
        pass

    @abstractmethod
    async def dist_table(self) -> str:
        pass
