import pytest
from src.utils import Storage, Logger


log = Logger(__name__)

@pytest.mark.asyncio
async def test_storage_connect():
    async with Storage() as storage:
        log.info('Storage connect successful.')
        assert storage != None

@pytest.mark.asyncio
async def test_storage_queryone():
    async with Storage() as storage:
        sql: str = 'select count(*) from station;'
        result = await storage.fetch_one(sql)
        count: int = int(result) # type: ignore
        assert count
        
        
@pytest.mark.asyncio
async def test_storage_querylist():
    async with Storage() as storage:
        sql = "select *  from station_60115400 where ts between '2026-01-01 12:00:00' and '2026-01-01 23:59:00';"
        result = await storage.fetch_row_list(sql)
        counts: int = len(result)
        assert counts
        