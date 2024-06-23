from typing import List
from datetime import datetime, timedelta
from core.model import WaterLevel
from util.tdenginetool import TDengineTool


# 查询指定日期的8点水位
async def select_waterlevel(date: datetime) -> List[WaterLevel]:
    sql = f"""SELECT `ts`, `current`, `stcd`, `name` FROM waterlevel WHERE `ts`='{date.strftime("%Y-%m-%d")} 08:00:00' """
    with TDengineTool() as td:
        result = td.query(sql)
        return [
            WaterLevel(
                tm=row[0][:-7],
                current=row[1],
                stcd=row[2],
                name=row[3],
            )
            for row in result
        ]


# 查询今天8点水位
async def today8_waterlevel() -> List[WaterLevel]:
    date_now = datetime.now()
    return await select_waterlevel(date_now)


# 查询昨天8点水位
async def yesterday8_waterlevel() -> List[WaterLevel]:
    yesterday = datetime.now() - timedelta(days=1)
    return await select_waterlevel(yesterday)


# 查询上周8点水位
async def lastweek8_waterlevel() -> List[WaterLevel]:
    one_week_ago = datetime.now() - timedelta(weeks=1)
    return await select_waterlevel(one_week_ago)


# 查询去年同期8点水位
async def lastyear8_waterlevel() -> List[WaterLevel]:
    now = datetime.now()
    last_year = now.replace(year=now.year - 1)
    return await select_waterlevel(last_year)
