from typing import List
from datetime import datetime, timedelta
from core.model import WaterLevel
from util.tdenginetool import TDengineTool


# 查询指定日期下的整点水位
async def select_waterlevel(date: datetime) -> List[WaterLevel]:
    sql = f"""SELECT `ts`, `current`, `stcd`, `name` FROM waterlevel WHERE `ts`='{date.strftime("%Y-%m-%d %H")}:00:00' """
    with TDengineTool() as td:
        result = td.query(sql)
        return [
            WaterLevel(
                tm=row[0][:-7],
                current=round(row[1], 2),  # 水位数据保留小数点后2位
                stcd=row[2],
                name=row[3],
            )
            for row in result
        ]


# 获取表1数据
async def table1_waterlevel():
    today = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    today_at_8 = await select_waterlevel(today)  # 今日8时
    yesterday_at_8 = await select_waterlevel(today - timedelta(days=1))  # 昨日8时
    one_week_ago_at_8 = await select_waterlevel(
        today - timedelta(weeks=1)
    )  # 上周同期8时
    last_year_at_8 = await select_waterlevel(
        today.replace(year=today.year - 1)
    )  # 去年同期8时
    return (today_at_8, yesterday_at_8, one_week_ago_at_8, last_year_at_8)


# 获取表2数据
async def table2_waterlevel():
    date_now = datetime.now()
    now_hour = await select_waterlevel(date_now)  # 当前时间的整点时刻数据
    yesterday_hour = await select_waterlevel(date_now - timedelta(days=1))  # 昨日8时
    return (now_hour, yesterday_hour)


# 获取表3数据
async def table3_waterlevel():
    date_now = datetime.now()
    now_hour = await select_waterlevel(date_now)  # 当前时间的整点时刻数据
    two_hour_ago = await select_waterlevel(
        date_now - timedelta(hours=2)
    )  # 前2小时整点时刻数据
    four_hour_ago = await select_waterlevel(
        date_now - timedelta(hours=4)
    )  # 前4小时整点时刻数据
    six_hour_ago = await select_waterlevel(
        date_now - timedelta(hours=6)
    )  # 前6小时整点时刻数据
    eight_hour_ago = await select_waterlevel(
        date_now - timedelta(hours=8)
    )  # 前8小时整点时刻数据
    ten_hour_ago = await select_waterlevel(
        date_now - timedelta(hours=10)
    )  # 前10小时整点时刻数据
    return (
        now_hour,
        two_hour_ago,
        four_hour_ago,
        six_hour_ago,
        eight_hour_ago,
        ten_hour_ago,
    )
