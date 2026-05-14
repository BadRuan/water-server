from typing import List, Dict, NamedTuple
from datetime import datetime, timedelta
from pathlib import Path
from abc import abstractmethod
from openpyxl import load_workbook
from openpyxl.styles import Font
from src.settings import station_list, COLOR, Station
from src.utils import Storage, Logger


log = Logger(__name__)

class PathRecoder(NamedTuple):
    source: str
    dist: str

def filePath(file_name: str) -> PathRecoder:
    base_dir = Path(__file__).resolve().parent.parent.parent
    source_path = base_dir / f"file/{file_name}.xlsx"
    dist_path = base_dir / f"dist/{file_name}.xlsx"
    return PathRecoder(source=str(source_path), dist=str(dist_path))

def today_or_yesterday(today, yesterday):
    current_hour: int = datetime.now().hour
    if current_hour > 10:
        return today
    else:
        return yesterday

# 数据库查询函数
async def get_station_data(station: Station, target_datetime: datetime) -> float:
    formatted_date: str = target_datetime.strftime("%Y-%m-%d %H:%M:%S")
    async with Storage() as storage:
        sql: str = f"select (height) from station_{station.code} where ts = '{formatted_date}';"
        log.debug(sql)
        result = await storage.fetch_row_one(sql)
        if result is None:
            return 0
        else:
            return result[0]
    return 0

# 时间描述的函数
def generate_time_description(hour_diff: int) -> str:
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

class DistXlsx:

    def __init__(self, file_name: str) -> None:
        self.path: PathRecoder = filePath(file_name)
        self.wb = load_workbook(self.path.source)  # 加载源文件
        self.sheet = self.wb.active  # 获取工作表

    def write_to_cell(self, location: str, value: float | str) -> None:
        if self.sheet is not None:
            self.sheet[location] = value

    # 更新填报日期时间
    def write_date(self) -> None:
        self.write_to_cell("A2",f"填报日期：{datetime.now().strftime('%Y年%m月%d日')}")

    # 填写每列标题
    def write_columns_head(self, table_head: Dict[str, str]):
        for loc, title in table_head.items():
            self.write_to_cell(loc, title)

    # 设置单元格样式
    def set_cell_style(self, locatoin: str, value: float, station: Station) -> None:
        if self.sheet is not None:
            cell = self.sheet[locatoin]
            if value >= station.sfsw and value < station.jjsw:
                cell.font = Font(color=COLOR.SheFang.value)
            elif value >= station.jjsw and value < station.bzsw:
                cell.font = Font(color=COLOR.JingJie.value, bold=True)
            elif value >= station.bzsw:
                cell.font = Font(color=COLOR.BaoZheng.value, bold=True)
            else:
                cell.font = Font(color=COLOR.Default.value)

    # 隐藏某列
    def hidden_column(self, hidden_column: List[str]) -> None:
        for column in hidden_column:
            self.sheet.column_dimensions[column].hidden = True # type: ignore

    # 填写每列数据
    async def write_cow_data(self, loc_list: List[str], target_datetimes: List[datetime]) -> None:
        # 为每个位置填充数据
        for column_item, target_datetime in zip(loc_list, target_datetimes): # example: [D5:D14]
            start , end = column_item.split(':') # ('D5', 'D14')
            lie_head: str = start[0] # 'D'
            index_list = range(int(start[1:]), int(end[1:])+1) # range(5, 15) = [5, 6, ... , 14]
            for station, index in zip(station_list, index_list):
                height: float = await get_station_data(station, target_datetime)
                log.debug(f"Cell: {lie_head}{index} => {station.name} : {height}")
                cell_location: str = lie_head + str(index)
                self.write_to_cell(cell_location, height)
                self.set_cell_style(cell_location, height, station)
            
    # 保存到目标路径
    def save(self) -> None:
        self.wb.save(self.path.dist)
    
    @abstractmethod
    async def dist(self) -> None:
        ...


class DistTable_1(DistXlsx):
    
    def __init__(self) -> None:
        super().__init__('table1')
    
    async def dist(self):
        self.write_date()

        target_datetimes: List[datetime] = [
            datetime.now().replace(hour=8, minute=0, second=0),  # 今日 8:00
            datetime.now().replace(hour=8, minute=0, second=0) - timedelta(days=1),  # 昨日 8:00
            datetime.now().replace(hour=8, minute=0, second=0) - timedelta(weeks=1),  # 上周 8:00
            datetime.now().replace(hour=8, minute=0, second=0) - timedelta(days=365),  # 去年今日 8:00
        ]
        data_locs: List[str] = ["D5:D14", "E5:E14", "F5:F14", "G5:G14"]
        await self.write_cow_data(data_locs, target_datetimes)

        self.save()

class DistTable_2(DistXlsx):
    
    def __init__(self) -> None:
        super().__init__('table2')
    
    async def dist(self):
        self.write_date()

        self.write_to_cell('D3',generate_time_description(0))
        self.write_to_cell('E3',generate_time_description(4))
        self.write_to_cell('F3',generate_time_description(8))

        target_datetimes: List[datetime] = [
            datetime.now().replace(minute=0, second=0),  # 当前时刻
            datetime.now().replace(minute=0, second=0) - timedelta(hours=4),  # 四小时前
            datetime.now().replace(minute=0, second=0) - timedelta(hours=8),  # 八小时前
        ]
        data_locs: List[str] = ["D5:D14", "E5:E14", "F5:F14"]
        await self.write_cow_data(data_locs, target_datetimes)

        self.save()
 
class DistTable_3(DistXlsx):
    
    def __init__(self) -> None:
        super().__init__('table3')
    
    async def dist(self):
        self.write_date()

        target_datetimes: List[datetime] = [
            datetime.now().replace(hour=8, minute=0, second=0),  # 今日 8:00
            datetime.now().replace(hour=8, minute=0, second=0) - timedelta(days=3),  # 三日前 8:00
            datetime.now().replace(hour=8, minute=0, second=0) - timedelta(days=365),  # 去年今日 8:00
        ]
        data_locs: List[str] = ["D5:D14", "E5:E14", "G5:G14"]
        await self.write_cow_data(data_locs, target_datetimes)

        self.save()
  
class DistTable_4(DistXlsx):
    
    def __init__(self) -> None:
        super().__init__('table4')
    
    async def dist(self):
        self.write_date()

        target_datetimes: List[datetime] = [
            datetime.now().replace(hour=8, minute=0, second=0),  # 今日 8:00
            datetime.now().replace(hour=8) - timedelta(days=1),  # 昨日 8:00
            datetime.now().replace(hour=8, minute=0, second=0) - timedelta(days=365),  # 去年今日 8:00
        ]
        data_locs: List[str] = ["D5:D14", "E5:E14", "G5:G14"]
        await self.write_cow_data(data_locs, target_datetimes)

        self.save()
       