from typing import List
from datetime import datetime, timedelta
from core.model import PathModel, Station, ColumnsHeadModel
from core.dao import table1_data, table2_data, table3_data
from util.xlsx import write_to_xlsx


async def get_table1(path: PathModel) -> str:
    # 列头的内容
    columns_head: ColumnsHeadModel = ColumnsHeadModel(
        loc_list=["D3", "E3", "F3", "G3"],
        titles=["今日8时", "昨日8时", "上周8时", "去年同期8时"],
    )
    # 水位数据位置
    talbe_loc: List[str] = [
        "D5:D14",
        "E5:E14",
        "F5:F14",
        "G5:G14",
    ]
    # 水位数据
    stations: List[Station] = await table1_data()
    await write_to_xlsx(path, columns_head, talbe_loc, stations)
    return path.dist


async def get_table2(path: PathModel) -> str:
    # 列头的内容
    now_hour = datetime.now().strftime("%H")
    columns_head: ColumnsHeadModel = ColumnsHeadModel(
        loc_list=["D3", "E3"],
        titles=[f"今日{now_hour}时", f"昨日{now_hour}时"],
    )

    # 水位数据位置
    talbe_loc: List[str] = ["D5:D14", "E5:E14"]

    # 水位数据
    stations: List[Station] = await table2_data()
    await write_to_xlsx(path, columns_head, talbe_loc, stations)
    return path.dist


async def get_table3(path: PathModel) -> str:
    # 列头的内容
    def datefunc(date: datetime) -> str:
        date = date.date()
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        if date == today:
            return "今日"
        elif date == yesterday:
            return "昨日"
        else:
            return "***"

    now_hour = datetime.now()
    two_hour_ago = now_hour - timedelta(hours=2)
    four_hour_ago = now_hour - timedelta(hours=4)
    six_hour_ago = now_hour - timedelta(hours=6)
    eight_hour_ago = now_hour - timedelta(hours=8)
    ten_hour_ago = now_hour - timedelta(hours=10)

    str1 = datefunc(now_hour) + now_hour.strftime("%H时")
    str2 = datefunc(two_hour_ago) + two_hour_ago.strftime("%H时")
    str3 = datefunc(four_hour_ago) + four_hour_ago.strftime("%H时")
    str4 = datefunc(six_hour_ago) + six_hour_ago.strftime("%H时")
    str5 = datefunc(eight_hour_ago) + eight_hour_ago.strftime("%H时")
    str6 = datefunc(ten_hour_ago) + ten_hour_ago.strftime("%H时")

    columns_head: ColumnsHeadModel = ColumnsHeadModel(
        loc_list=["D3", "E3", "F3", "G3", "H3", "I3"],
        titles=[str1, str2, str3, str4, str5, str6],
    )
    
    # 水位数据位置
    talbe_loc: List[str] = ["D5:D14", "E5:E14","F5:F14","G5:G14","H5:H14","I5:I14"]

    # 水位数据
    stations: List[Station] = await table3_data()
    await write_to_xlsx(path, columns_head, talbe_loc, stations)
    return path.dist