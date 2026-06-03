from typing import List, Dict, NamedTuple
from datetime import datetime, timedelta
from pathlib import Path
from os.path import exists
from os import remove
from openpyxl import load_workbook
from openpyxl.styles import Font
from dateutil.relativedelta import relativedelta
from src.settings import station_list, COLOR, Station
from src.utils import get_logger, fetch_one


log = get_logger(__name__)


class PathRecorder(NamedTuple):
    source: str
    dist: str


def delete_file_if_exists(file_path: str) -> None:
    if exists(file_path):
        try:
            remove(file_path)
        except PermissionError:
            log.error(f"权限不足，无法删除：{file_path}")
        except Exception:
            log.error(f"删除文件时发生未知错误：{file_path}")


def file_path(file_name: str) -> PathRecorder:
    base_dir = Path(__file__).resolve().parent.parent.parent
    source_path = base_dir / f"file/{file_name}.xlsx"
    dist_path = base_dir / f"dist/{file_name}.xlsx"
    delete_file_if_exists(str(dist_path))
    return PathRecorder(source=str(source_path), dist=str(dist_path))


# 数据库查询函数 — 参数化查询，防止 SQL 注入
async def get_station_data(station: Station, target_datetime: datetime) -> float:
    sql = f"SELECT height FROM station_{station.code} WHERE ts = date_trunc('second', $1::timestamp)"
    result = await fetch_one(sql, target_datetime)
    return result if result is not None else 0


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
    """Excel 水位表生成器基类，支持上下文管理器自动关闭。"""

    def __init__(self, file_name: str) -> None:
        self.path: PathRecorder = file_path(file_name)
        self.wb = load_workbook(self.path.source)
        self.sheet = self.wb.active

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def close(self):
        if self.wb:
            self.wb.close()

    def write_to_cell(self, location: str, value: float | str) -> None:
        if self.sheet is not None:
            self.sheet[location] = value

    def write_date(self) -> None:
        self.write_to_cell("A2", f"填报日期：{datetime.now().strftime('%Y年%m月%d日')}")

    def write_columns_head(self, table_head: Dict[str, str]):
        for loc, title in table_head.items():
            self.write_to_cell(loc, title)

    def set_cell_style(self, location: str, value: float, station: Station) -> None:
        if self.sheet is not None:
            cell = self.sheet[location]
            if station.sfsw <= value < station.jjsw:
                cell.font = Font(color=COLOR.SheFang.value)
            elif station.jjsw <= value < station.bzsw:
                cell.font = Font(color=COLOR.JingJie.value, bold=True)
            elif value >= station.bzsw:
                cell.font = Font(color=COLOR.BaoZheng.value, bold=True)
            else:
                cell.font = Font(color=COLOR.Default.value)

    def hidden_column(self, columns: List[str]) -> None:
        for column in columns:
            self.sheet.column_dimensions[column].hidden = True  # type: ignore

    async def write_column_data(self, loc_list: List[str], target_datetimes: List[datetime]) -> None:
        """按列填充各站点水位数据。loc_list 格式如 ["D5:D14"]。"""
        for column_item, target_datetime in zip(loc_list, target_datetimes):
            log.debug(f'目标时间：{target_datetime}')
            start, end = column_item.split(':')
            col_letter: str = start[0]
            index_range = range(int(start[1:]), int(end[1:]) + 1)
            for station, row_index in zip(station_list, index_range):
                height: float = await get_station_data(station, target_datetime)
                cell_location: str = col_letter + str(row_index)
                self.write_to_cell(cell_location, height)
                self.set_cell_style(cell_location, height, station)

    def save(self) -> None:
        self.wb.save(self.path.dist)


class DistTable_1(DistXlsx):

    def __init__(self) -> None:
        super().__init__('table1')

    async def dist(self):
        with self:
            self.write_date()
            now: datetime = datetime.now().replace(hour=8, minute=0, second=0)
            target_datetimes: List[datetime] = [
                now,
                now - timedelta(days=1),
                now - timedelta(weeks=1),
                now - relativedelta(years=1),
            ]
            data_locs: List[str] = ["D5:D14", "E5:E14", "F5:F14", "G5:G14"]
            await self.write_column_data(data_locs, target_datetimes)
            self.save()


class DistTable_2(DistXlsx):

    def __init__(self) -> None:
        super().__init__('table2')

    async def dist(self):
        with self:
            self.write_date()
            self.write_to_cell('D3', generate_time_description(0))
            self.write_to_cell('E3', generate_time_description(4))
            self.write_to_cell('F3', generate_time_description(8))

            now_rounded = datetime.now().replace(minute=0, second=0)
            target_datetimes: List[datetime] = [
                now_rounded,
                now_rounded - timedelta(hours=4),
                now_rounded - timedelta(hours=8),
            ]
            data_locs: List[str] = ["D5:D14", "E5:E14", "F5:F14"]
            await self.write_column_data(data_locs, target_datetimes)
            self.save()


class DistTable_3(DistXlsx):

    def __init__(self) -> None:
        super().__init__('table3')

    async def dist(self):
        with self:
            self.write_date()
            now_8am = datetime.now().replace(hour=8, minute=0, second=0)
            target_datetimes: List[datetime] = [
                now_8am,
                now_8am - timedelta(days=3),
                now_8am - timedelta(days=365),
            ]
            data_locs: List[str] = ["D5:D14", "E5:E14", "G5:G14"]
            await self.write_column_data(data_locs, target_datetimes)
            self.save()


class DistTable_4(DistXlsx):

    def __init__(self) -> None:
        super().__init__('table4')

    async def dist(self):
        with self:
            self.write_date()
            now_8am = datetime.now().replace(hour=8, minute=0, second=0)
            target_datetimes: List[datetime] = [
                now_8am,
                now_8am - timedelta(days=1),
                now_8am - relativedelta(years=1),
            ]
            data_locs: List[str] = ["D5:D14", "E5:E14", "G5:G14"]
            await self.write_column_data(data_locs, target_datetimes)
            self.save()
