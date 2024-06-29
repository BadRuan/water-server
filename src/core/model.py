from pydantic import BaseModel
from typing import List


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


# 水位测站基础参数
class Station(BaseModel):
    stcd: int
    name: str
    sfsw: float
    jjsw: float
    bzsw: float
    waterline: List[float] = []
