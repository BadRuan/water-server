from typing import List, Dict
from abc import abstractmethod
from datetime import datetime, timedelta
from core.model import Station
from core.dao import TableDao, Table1_Dao, Table2_Dao, Table3_Dao
from util.xlsx import DataToXlsx
from util.othertool import today_or_yesterday


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


class Table1_Service(TableService):

    def __init__(self) -> None:
        dao: TableDao = Table1_Dao()
        xlsx: DataToXlsx = DataToXlsx(source="table1", dist="dist1")
        super().__init__(dao, xlsx)

    def write_table_head(self):
        # 表头信息和位置
        table_head: Dict[str, str] = {
            "D3": "今日8时",
            "E3": "昨日8时",
            "F3": "上周8时",
            "G3": "去年同期8时",
        }
        self.xlsx.write_columns_head(table_head)

    async def write_table_data(self):
        # 数据列位置
        data_locs: List[str] = [
            "D5:D14",
            "E5:E14",
            "F5:F14",
            "G5:G14",
            "H5:H14",
            "I5:I14",
        ]
        datas: List[Station] = await self.dao.get_table_data()
        self.xlsx.write_cow_data(data_locs, datas)

    async def get_table(self) -> str:
        self.xlsx.write_date()  # 更新表格日期
        self.write_table_head()  # 按表头位置写入信息
        await self.write_table_data()  # 填写表格数据
        self.xlsx.save()
        return self.xlsx.path.dist


class Table2_Service(TableService):

    def __init__(self) -> None:
        dao: TableDao = Table2_Dao()
        xlsx: DataToXlsx = DataToXlsx(source="table2", dist="dist2")
        super().__init__(dao, xlsx)

    def write_table_head(self):
        # 表头信息和位置
        table_head: Dict[str, str] = {
            "D3": self.generate_time_description(0),
            "E3": self.generate_time_description(2),
            "F3": "",
            "H3": "两小时内",
        }
        table_head["F3"] = today_or_yesterday("今日8时", "昨日8时")
        self.xlsx.write_columns_head(table_head)

    async def write_table_data(self):
        # 数据列位置
        data_locs: List[str] = ["D5:D14", "E5:E14", "F5:F14"]
        datas: List[Station] = await self.dao.get_table_data()
        self.xlsx.write_cow_data(data_locs, datas)

    async def get_table(self) -> str:
        self.xlsx.write_date()  # 更新表格日期
        self.write_table_head()  # 按表头位置写入信息
        await self.write_table_data()  # 填写表格数据
        self.xlsx.hidden_column(["E"])  # 隐藏E列
        self.xlsx.save()
        return self.xlsx.path.dist


class Table3_Service(TableService):

    def __init__(self) -> None:
        dao: TableDao = Table3_Dao()
        xlsx: DataToXlsx = DataToXlsx(source="table3", dist="dist3")
        super().__init__(dao, xlsx)

    def write_table_head(self):
        # 表头信息和位置
        table_head: Dict[str, str] = {
            "D3": self.generate_time_description(0),
        }
        table_head["E3"] = today_or_yesterday("今日8时", "昨日8时")
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