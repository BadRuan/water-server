from pydantic import BaseModel
from typing import List


class DatabaseConfig(BaseModel):
    url: str
    port: int
    user: str
    password: str
    database: str


class WaterLevel(BaseModel):
    tm: str
    z: float
    stcd: int
    name: str


class Station(BaseModel):
    stcd: int
    name: str
    sfsw: float
    jjsw: float
    bzsw: float
    waterline: List[float] = []


class ApiStation(BaseModel):
    name: str
    count: int
