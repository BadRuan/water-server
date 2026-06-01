from typing import List, Any, Optional
from contextlib import asynccontextmanager
from asyncpg import create_pool, Pool
from src.settings import settings
from src.utils import Logger


log = Logger(__name__)
_db_pool: Optional[Pool] = None


async def init_db_pool():
    """应用启动时调用，初始化全局连接池"""
    global _db_pool
    if _db_pool is None:
        async def set_timezone(connection):
            await connection.execute(f"SET TIME ZONE '{settings.TIMEZONE}';")
        
        _db_pool = await create_pool(
            dsn=settings.DATABASE_URL,
            min_size=5,          # 最小连接数
            max_size=20,         # 最大连接数，根据实际并发量调整
            init=set_timezone,   # 初始化连接时的回调
            max_inactive_connection_lifetime=300.0 # 空闲连接回收时间
        )

async def close_db_pool():
    """应用关闭时调用，释放连接池资源"""
    global _db_pool
    if _db_pool:
        await _db_pool.close()
        _db_pool = None

@asynccontextmanager
async def get_db_connection():
    """获取连接的上下文管理器，从全局池中借用和归还连接"""
    if not _db_pool:
        raise RuntimeError("数据库连接池未初始化，请先调用 init_db_pool()")
    
    async with _db_pool.acquire() as conn:
        yield conn

async def fetch_one(sql: str) -> Optional[Any]:
    log.info(sql)
    async with get_db_connection() as s:
        result: Any = await s.fetchval(sql)
        return result

async def fetch_row_one(sql: str) -> Optional[Any]:
    log.info(sql)
    async with get_db_connection() as s:
        return await s.fetchrow(sql)

async def fetch_row_list(sql: str) -> List[Any]:
    log.info(sql)
    async with get_db_connection() as s:
        return await s.fetch(sql)