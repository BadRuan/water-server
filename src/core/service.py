from typing import List, Dict
from datetime import datetime, timedelta
from core.model import Station
from core.dao import table1_data, table2_data, table3_data, table4_data
from util.xlsx import write_to_xlsx
from util.othertool import PathModel, filePath, today_or_yesterday


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
    pathModel: PathModel,
    table_head: Dict[str, str],
    data_locs: List[str],
    data_func,
    hidden_column: List[str],
) -> str:
    stations: List[Station] = await data_func()
    await write_to_xlsx(pathModel, table_head, data_locs, stations, hidden_column)
    return pathModel.dist


# 获取表1数据的异步函数
async def get_table1() -> str:
    path: PathModel = filePath(source="table1", dist="dist1")
    # 表头信息和位置
    table_head: Dict[str, str] = {
        "D3": "今日8时",
        "E3": "昨日8时",
        "F3": "上周8时",
        "G3": "去年同期8时",
    }
    # 数据列位置
    data_locs: List[str] = ["D5:D14", "E5:E14", "F5:F14", "G5:G14", "H5:H14", "I5:I14"]
    return await fetch_table_data(path, table_head, data_locs, table1_data, [])


# 获取表2数据的异步函数
async def get_table2() -> str:
    path: PathModel = filePath(source="table2", dist="dist2")
    # 表头信息和位置
    table_head: Dict[str, str] = {
        "D3": generate_time_description(0),
        "E3": generate_time_description(2),
        "F3": "",
    }
    table_head["F3"] = today_or_yesterday("今日8时", "昨日8时")
    data_locs: List[str] = ["D5:D14", "E5:E14", "F5:F14"]
    return await fetch_table_data(path, table_head, data_locs, table2_data, ['E'])


# 获取表3数据的异步函数
async def get_table3() -> str:
    path: PathModel = filePath(source="table3", dist="dist3")
    # 表头信息和位置
    time_description = [generate_time_description(i) for i in range(0, 12, 2)]
    table_head: Dict[str, str] = {
        "D3": time_description[0],
        "E3": time_description[1],
        "F3": time_description[2],
        "G3": time_description[3],
        "H3": time_description[4],
        "I3": time_description[5],
    }
    data_locs: List[str] = ["D5:D14", "E5:E14", "F5:F14", "G5:G14", "H5:H14", "I5:I14"]
    return await fetch_table_data(path, table_head, data_locs, table3_data, [])


# 获取表4数据的异步函数
async def get_table4() -> str:
    path: PathModel = filePath(source="table3", dist="dist4")
    # 表头信息和位置
    time_description = [generate_time_description(i) for i in range(0, 6)]
    table_head: Dict[str, str] = {
        "D3": time_description[0],
        "E3": time_description[1],
        "F3": time_description[2],
        "G3": time_description[3],
        "H3": time_description[4],
        "I3": time_description[5],
    }
    data_locs: List[str] = ["D5:D14", "E5:E14", "F5:F14", "G5:G14", "H5:H14", "I5:I14"]
    return await fetch_table_data(path, table_head, data_locs, table4_data, [])
