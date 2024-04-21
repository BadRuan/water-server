from pydantic import BaseModel
from typing import List
from util.tdenginetool import TDengineTool


class WaterLevel(BaseModel):
    tm: str
    current: float
    stcd: int
    name: str


# 查询当前最新水位
def select_cruuent_waterlevel() -> List[WaterLevel]:
    with TDengineTool() as td:
        SQL = "SELECT LAST_ROW(ts) as tm, `current`, `STCD`, `NAME` FROM waterlevel GROUP BY `STCD`"
        result = td.query(SQL)
        return [
            WaterLevel(tm=row[0], current=row[1], stcd=row[2], name=row[3])
            for row in result
        ]
