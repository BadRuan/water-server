from typing import List, Dict
from abc import abstractmethod
from datetime import datetime, timedelta
from core.model import Station
from core.dao import TableDao, Table3_Dao
from util.xlsx import DataToXlsx


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
    async def write_table_data(self):
        pass

    @abstractmethod
    async def get_table(self) -> str:
        pass


class Table3_Service(TableService):

    def __init__(self) -> None:
        dao: TableDao = Table3_Dao()
        xlsx: DataToXlsx = DataToXlsx(source="table3", dist="dist3")
        super().__init__(dao, xlsx)

    def write_table_head(self):
        # 表头信息和位置
        table_head: Dict[str, str] = {
            "D3": "今日8时",
            "E3": "昨日8时"
        }
        self.xlsx.write_columns_head(table_head)

    async def write_table_data(self):
        # 数据列位置
        data_locs: List[str] = ["D5:D14", "E5:E14"]
        datas: List[Station] = await self.dao.get_table_data()
        self.xlsx.write_cow_data(data_locs, datas)

    async def get_table(self) -> str:
        self.xlsx.write_date()  # 更新表格日期
        self.write_table_head()  # 按表头位置写入信息
        await self.write_table_data()  # 填写表格数据
        self.xlsx.save()
        return self.xlsx.path.dist