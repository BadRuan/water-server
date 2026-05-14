from typing import List, Any, Optional
from asyncpg import connect
from src.settings import postgres


class Storage():   
    def __init__(self) -> None:
        self.connection = None
    
    async def __aenter__(self):
        await self.init_connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection is not None:
            await self.connection.close()
            
    async def init_connect(self):
        self.connection = await connect(host=postgres.url, user=postgres.user, password=postgres.password, port=postgres.port, database=postgres.database, server_settings={
            'timezone': 'UTC'
        })
    
    async def fetch_one(self,sql: str) -> Optional[Any]:
        if self.connection is not None:
            result: Any = await self.connection.fetchval(sql)
            return result
        else:
            return None
        
    async def fetch_row_one(self, sql: str) -> Optional[Any]:
        if self.connection is not None:
            result = await self.connection.fetchrow(sql)
            if result is None:
                return []
            else:
                return result
        else:
            return []
        
    async def fetch_row_list(self, sql: str) -> List[Any]:
        if self.connection is not None:
            return await self.connection.fetch(sql)
        else:
            return []
            