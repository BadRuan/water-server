from typing import List
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font
from core.settings import SF_COLOR, JJ_COLOR, BZ_COLOR
from core.model import PathModel, ColumnsHeadModel, Station


# 填写每列标题
def writeColumnsHead(sheet, columns_head: ColumnsHeadModel):
    for loc, title in zip(columns_head.loc_list, columns_head.titles):
        sheet[loc] = title
    return sheet


# 填写每列数据
def writeCowData(sheet, loc_list, stations):
    def func(index: int, talbe_loc: str):
        for row, station in zip(sheet[talbe_loc], stations):
            for cell in row:
                w_value = station.waterline[index]
                cell.value = w_value
                # 根据数值情况标注颜色
                if w_value >= station.sfsw and w_value < station.jjsw:
                    cell.font = Font(color=SF_COLOR)
                elif w_value >= station.jjsw and w_value < station.bzsw:
                    cell.font = Font(color=JJ_COLOR, bold=True)
                elif w_value >= station.bzsw:
                    cell.font = Font(color=BZ_COLOR, bold=True)

    for index, loc in enumerate(loc_list):
        func(index, loc)
    return sheet


# 填写表格内容
async def write_to_xlsx(
    path: PathModel,
    columns_head: ColumnsHeadModel,
    talbe_loc: List[str],
    stations: List[Station],
):
    wb = load_workbook(path.source)  # 读取文件
    sheet1 = wb.active  # 默认子表
    # 更新填报日期和时间
    sheet1["A2"] = "填报日期： " + datetime.now().strftime("%Y年%m月%d日 %H时")

    # 填写标题
    sheet1 = writeColumnsHead(sheet1, columns_head)
    # 填写对应水位数据

    sheet1 = writeCowData(sheet1, talbe_loc, stations)

    wb.save(path.dist)

