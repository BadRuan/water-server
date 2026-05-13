from typing import List, Any, Optional
from asyncpg import connect
from src.settings import postgres


class Storage():   
    def __init__(self) -> None:
        self.connection = None
        self.initialized = None
    
    async def __aenter__(self):
        await self.ensure_initialized()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection is not None:
            await self.connection.close()
    
    async def ensure_initialized(self):
        if self.initialized is None:
            await self.init_connect()
            
    async def init_connect(self):
        self.connection = await connect(host=postgres.url, user=postgres.user, password=postgres.password, port=postgres.port, database=postgres.database, server_settings={
            'timezone': 'UTC'  # 设置时区，例如 'UTC' 或 'Asia/Shanghai'
        })
                   
    async def query_one(self, sql: str) -> Optional[Any]:
        if self.connection is not None:
            result = await self.connection.fetchrow(sql)
            if result is None:
                return None
            else:
                return result
        else:
            return ''
        
    async def query_list(self, sql: str) -> List[Any]:
        if self.connection is not None:
            return await self.connection.fetch(sql)
        else:
            return []
            