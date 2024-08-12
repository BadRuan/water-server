from typing import List, Dict
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font
from core.settings import DEFAULT_COLOR, SF_COLOR, JJ_COLOR, BZ_COLOR
from core.model import Station
from util.othertool import PathModel, filePath


class DataToXlsx:

    def __init__(self, source: str, dist: str) -> None:
        self.path: PathModel = filePath(source, dist)
        self.wb = load_workbook(self.path.source)  # 加载源文件
        self.sheet = self.wb.active  # 获取工作表

    # 更新填报日期时间
    def write_date(self):
        self.sheet["A2"] = f"填报日期：{datetime.now().strftime('%Y年%m月%d日 %H时')}"

    # 填写每列标题
    def write_columns_head(self, table_head: Dict[str, str]):
        for loc, title in table_head.items():
            self.sheet[loc] = title

    # 设置单元格样式
    def set_cell_style(self, cell, value, sfsw, jjsw, bzsw):
        if value >= sfsw and value < jjsw:
            cell.font = Font(color=SF_COLOR)
        elif value >= jjsw and value < bzsw:
            cell.font = Font(color=JJ_COLOR, bold=True)
        elif value >= bzsw:
            cell.font = Font(color=BZ_COLOR, bold=True)
        else:
            cell.font = Font(color=DEFAULT_COLOR)

    # 隐藏某列
    def hidden_column(self, hidden_column: List[str]):
        for column in hidden_column:
            self.sheet.column_dimensions[column].hidden = True

    # 填写每列数据
    def write_cow_data(self, loc_list: List[str], stations: List[Station]):
        # 为每个位置填充数据
        for loc, index in zip(loc_list, range(len(loc_list))):
            for row, station in zip(self.sheet[loc], stations):
                try:
                    # 使用安全的索引访问，防止越界错误
                    w_value = station.waterline[index]
                except IndexError:
                    # 如果waterline列表长度不足，则使用0填充
                    w_value = 0
                finally:
                    row[0].value = w_value

                # 设置字体颜色和加粗样式
                self.set_cell_style(
                    row[0], w_value, station.sfsw, station.jjsw, station.bzsw
                )

    # 保存到目标路径
    def save(self):
        self.wb.save(self.path.dist)  
