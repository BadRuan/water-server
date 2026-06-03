import pytest
from src.settings import station_list
from src.dao import DistTable_1, DistTable_4
from src.utils import get_logger, init_db_pool

log = get_logger(__name__)


@pytest.mark.asyncio
async def test_dist_table_1():
    await init_db_pool()
    d1 = DistTable_1()
    await d1.dist()
