from typing import NamedTuple
from dataclasses import dataclass
from datetime import datetime


class DataConfig(NamedTuple):
    url: str
    user: str
    password: str
    port: int
    database: str

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
    timestamp: datetime
