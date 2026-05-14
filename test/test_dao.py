import pytest
from src.dao import DistTable_1
from src.utils import Logger


log = Logger(__name__)

@pytest.mark.asyncio
async def test_dist_table_1():
    d1 = DistTable_1()
    await d1.dist()
   