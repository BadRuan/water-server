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


async def table1_waterlevel():
    date_now = datetime.now()
    today = await select_waterlevel(date_now)
    yesterday = await select_waterlevel(date_now - timedelta(days=1))
    one_week_ago = await select_waterlevel(date_now - timedelta(weeks=1))
    last_year = await select_waterlevel(date_now.replace(year=date_now.year - 1))
    return (today, yesterday, one_week_ago, last_year)


async def table2_waterlevel():
    date_now = datetime.now()
    now_hour = await select_waterlevel(date_now)
    two_hour_ago = await select_waterlevel(date_now - timedelta(hours=2))
    four_hour_ago = await select_waterlevel(date_now - timedelta(hours=4))
    six_hour_ago = await select_waterlevel(date_now - timedelta(hours=6))
    eight_hour_ago = await select_waterlevel(date_now - timedelta(hours=8))
    ten_hour_ago = await select_waterlevel(date_now - timedelta(hours=10))
    return (
        now_hour,
        two_hour_ago,
        four_hour_ago,
        six_hour_ago,
        eight_hour_ago,
        ten_hour_ago,
    )
