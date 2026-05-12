import pytest
from src.dao import DistTable_1, DistTable_2, DistTable_3, DistTable_4
from src.utils import Logger


log = Logger(__name__)

@pytest.mark.asyncio
async def test_dist_table_1():
    d1 = DistTable_1()
    d2 = DistTable_2()
    d3 = DistTable_3()
    d4 = DistTable_4()
    await d1.dist()
    await d2.dist()
    await d3.dist()
    await d4.dist()
   