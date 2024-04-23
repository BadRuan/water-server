from pydantic import BaseModel
from typing import Optional
from model.settings import Station


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
    station_name: Optional[str] = ''
    current: Optional[float] = 0
