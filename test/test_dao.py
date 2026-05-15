import pytest
from datetime import datetime
from src.settings import station_list
from src.dao import get_station_data, DistTable_1
from src.utils import Logger


log = Logger(__name__)

@pytest.mark.asyncio
async def test_dist_table_1():
    d1 = DistTable_1()
    await d1.dist()

@pytest.mark.asyncio
async def test_get_staion_data():
    data: float = await get_station_data(station_list[0], datetime.now().replace(hour=8, minute=0, second=0))
    log.info(f"==> data {data}")
    