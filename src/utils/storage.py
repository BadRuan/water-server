from typing import List, Any, Optional
from contextlib import asynccontextmanager
from asyncpg import create_pool, Pool
from src.settings import settings
from src.utils.logger import get_logger


log = get_logger(__name__)
_db_pool: Optional[Pool] = None


async def init_db_pool():
    """应用启动时调用，初始化全局连接池"""
    global _db_pool
    if _db_pool is None:
        async def set_timezone(connection):
            await connection.execute(f"SET TIME ZONE '{settings.TIMEZONE}';")

        _db_pool = await create_pool(
            dsn=settings.DATABASE_URL,
            min_size=5,
            max_size=20,
            init=set_timezone,
            max_inactive_connection_lifetime=300.0,
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


async def fetch_one(sql: str, *args: Any) -> Optional[Any]:
    """执行查询并返回单个值（第一行第一列）"""
    async with get_db_connection() as conn:
        return await conn.fetchval(sql, *args)


async def fetch_row_one(sql: str, *args: Any) -> Optional[Any]:
    """执行查询并返回一行记录"""
    async with get_db_connection() as conn:
        return await conn.fetchrow(sql, *args)


async def fetch_row_list(sql: str, *args: Any) -> List[Any]:
    """执行查询并返回多行记录"""
    async with get_db_connection() as conn:
        return await conn.fetch(sql, *args)
