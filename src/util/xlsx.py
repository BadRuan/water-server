from typing import List, Dict
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font
from core.settings import SF_COLOR, JJ_COLOR, BZ_COLOR
from util.othertool import PathModel
from core.model import Station


# 填写每列标题
def write_columns_head(sheet, table_head: Dict[str, str]):
    for loc, title in table_head.items():
        sheet[loc] = title
    return sheet


# 填写每列数据
def write_cow_data(sheet, loc_list, stations):
    # 为每个位置填充数据
    for loc, index in zip(loc_list, range(len(loc_list))):
        for row, station in zip(sheet[loc], stations):
            try:
                # 使用安全的索引访问，防止越界错误
                w_value = station.waterline[index]
            except IndexError:
                # 如果waterline列表长度不足，则使用0填充
                w_value = 0
            finally:
                row[0].value = w_value

            # 设置字体颜色和加粗样式
            set_cell_style(row[0], w_value, station.sfsw, station.jjsw, station.bzsw)
    return sheet


# 设置单元格样式
def set_cell_style(cell, value, sfsw, jjsw, bzsw):
    if value >= sfsw and value < jjsw:
        cell.font = Font(color=SF_COLOR)
    elif value >= jjsw and value < bzsw:
        cell.font = Font(color=JJ_COLOR, bold=True)
    elif value >= bzsw:
        cell.font = Font(color=BZ_COLOR, bold=True)


# 填写表格内容
async def write_to_xlsx(
    path: PathModel,
    table_head: Dict[str, str],
    data_locs: List[str],
    stations: List[Station],
    hidden_column: List[str],
):
    wb = load_workbook(path.source)  # 加载源文件
    sheet = wb.active  # 获取活动工作表

    # 更新填报日期和时间
    sheet["A2"] = f"填报日期：{datetime.now().strftime('%Y年%m月%d日 %H时')}"

    # 填写标题
    sheet = write_columns_head(sheet, table_head)
    # 填写对应水位数据
    sheet = write_cow_data(sheet, data_locs, stations)

    # 隐藏某列
    for column in hidden_column:
        sheet.column_dimensions[column].hidden = True

    wb.save(path.dist)  # 保存到目标路径
