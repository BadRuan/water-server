from typing import List
from pydantic import BaseModel


class ApiStation(BaseModel):
    name: str
    count: int


class DataModel(BaseModel):
    total_count: int
    this_year_count: int
    count_by_station: List[ApiStation]
    this_year_count_by_station: List[ApiStation]
