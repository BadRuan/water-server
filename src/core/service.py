from typing import List
from datetime import datetime, timedelta
from core.model import PathModel, Station, ColumnsHeadModel
from core.dao import table1_data, table2_data, table3_data, table4_data
from util.xlsx import write_to_xlsx


# 定义一个生成时间描述的函数
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


# 定义一个获取表格数据的通用函数
async def fetch_table_data(
    path: PathModel, data_func, locs: List[str], headers: List[str]
) -> str:
    columns_head: ColumnsHeadModel = ColumnsHeadModel(loc_list=locs, titles=headers)
    stations: List[Station] = await data_func()
    await write_to_xlsx(path, columns_head, locs, stations)
    return path.dist


# 获取表1数据的异步函数
async def get_table1(path: PathModel) -> str:
    # 表头信息和数据位置
    locs = ["D3", "E3", "F3", "G3"]
    headers = ["今日8时", "昨日8时", "上周8时", "去年同期8时"]
    return await fetch_table_data(path, table1_data, locs, headers)


# 获取表2数据的异步函数
async def get_table2(path: PathModel) -> str:
    # 生成表头信息
    headers = [generate_time_description(0), generate_time_description(2)]
    # 数据位置
    locs = ["D3", "E3"]
    return await fetch_table_data(path, table2_data, locs, headers)


# 获取表3数据的异步函数
async def get_table3(path: PathModel) -> str:
    # 生成表头信息
    headers = [generate_time_description(i) for i in range(0, 12, 2)]
    # 数据位置
    locs = ["D3", "E3", "F3", "G3", "H3", "I3"]
    return await fetch_table_data(path, table3_data, locs, headers)


# 获取表4数据的异步函数
async def get_table4(path: PathModel) -> str:
    # 生成表头信息
    headers = [generate_time_description(i) for i in range(0, 6)]
    # 数据位置
    locs = ["D3", "E3", "F3", "G3", "H3", "I3"]
    return await fetch_table_data(path, table4_data, locs, headers)
