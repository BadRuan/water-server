from typing import NamedTuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Station:
    code: int 
    name: str
    sfsw: float
    jjsw: float
    bzsw: float


class WaterItem(NamedTuple):
    code: int 
    height: float
    yesterday_height: float
    timestamp: datetime
