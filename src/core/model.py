from pydantic import BaseModel
from typing import Optional


# 数据库参数格式
class Database(BaseModel):
    url: str
    port: int
    user: str
    password: str
    database: str


# 水文站参数格式
class Station(BaseModel):
    stcd: int
    name: str


class WaterLevel(BaseModel):
    tm: str
    current: float
    stcd: int
    name: str


# 三线水位参数格式
class ThreeLine(BaseModel):
    stcd: int
    sfsw: float
    jjsw: float
    bzsw: float
    name: str
    station_name: Optional[str] = ""
    current: Optional[float] = 0
