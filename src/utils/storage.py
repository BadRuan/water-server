from typing import List, Any, Optional
from contextlib import asynccontextmanager
from asyncpg import create_pool
from src.settings import settings


async def set_timezone(connection):
    await connection.execute(f"SET TIME ZONE '{settings.TIMEZONE}';")

@asynccontextmanager
async def storage():
    pool = await create_pool(dsn=settings.DATABASE_URL, init=set_timezone)
    try:    
        yield pool
    except Exception:
        raise
    finally:
        await pool.close()    

async def fetch_one(sql: str) -> Optional[Any]:
    async with storage() as s:
        result: Any = await s.fetchval(sql)
        return result

async def fetch_row_one(sql: str) -> Optional[Any]:
    async with storage() as s:
        return await s.fetchrow(sql)

async def fetch_row_list(sql: str) -> List[Any]:
    async with storage() as s:
        return await s.fetch(sql)