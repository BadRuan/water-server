from typing import List, Dict
from model import Station
from utils.xlsx import DataToXlsx
from utils.othertool import today_or_yesterday
from dao.table_dao import TableDao,Table1_Dao
from service.base_service import TableService


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
            "G3": "去年同期",
        }
        self.xlsx.write_columns_head(table_head)

    def write_data_to_table(self):
        # 数据列位置
        data_locs: List[str] = ["D5:D14", "E5:E14", "F5:F14", "G5:G14"]
        datas: List[Station] = self.dao.get_table_data()
        self.xlsx.write_cow_data(data_locs, datas)

    def dist_table(self) -> str:
        self.xlsx.write_date()  # 更新表格日期
        self.write_table_head()  # 按表头位置写入信息
        self.write_data_to_table()  # 填写表格数据
        self.xlsx.save()
        return self.xlsx.path.dist

class Table2_Service(TableService):

    def __init__(self) -> None:
        dao: TableDao = Table1_Dao()
        xlsx: DataToXlsx = DataToXlsx(source="table2", dist="dist2")
        super().__init__(dao, xlsx)

    def write_table_head(self):
        # 表头信息和位置
        table_head: Dict[str, str] = {
            "D3": self.generate_time_description(0),
            "E3": self.generate_time_description(4),
            "F3": self.generate_time_description(8),
        }
        self.xlsx.write_columns_head(table_head)

    def write_data_to_table(self):
        # 数据列位置
        data_locs: List[str] = ["D5:D14", "E5:E14", "F5:F14"]
        datas: List[Station] = self.dao.get_table_data()
        self.xlsx.write_cow_data(data_locs, datas)

    def dist_table(self) -> str:
        self.xlsx.write_date()  # 更新表格日期
        self.write_table_head()  # 按表头位置写入信息
        self.write_data_to_table()  # 填写表格数据
        self.xlsx.save()
        return self.xlsx.path.dist
