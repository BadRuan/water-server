from pydantic import BaseModel
from typing import Optional


# 数据库参数格式
class Database(BaseModel):
    url: str
    port: int
    user: str
    password: str
    database: str


class WaterLevel(BaseModel):
    tm: str
    current: float
    stcd: int
    name: str


# 水文站参数格式
class Station(BaseModel):
    stcd: int
    name: str
    sfsw: float
    jjsw: float
    bzsw: float
    today_8: Optional[float] = 0
    yesterday_8: Optional[float] = 0
