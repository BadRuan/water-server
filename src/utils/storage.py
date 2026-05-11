from typing import List, Any, Optional
from psycopg2 import connect as pq_connect
from src.settings import postgres


class Storage():   
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None
        self.initialized = None
    
    def __enter__(self):
        self.ensure_initialized()
        return self
    
    def __exit__(self, exc_type, exc, tb):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()
    
    def ensure_initialized(self):
        if self.initialized is None:
            self.init_connect()
            
    def execute(self) -> None:
        self.ensure_initialized()

    def init_connect(self):
        self.connection = pq_connect(host=postgres.url, user=postgres.user, password=postgres.password, port=postgres.port, database=postgres.database)
        if self.connection is not None:    
            self.cursor = self.connection.cursor()
              
    def save(self, sql: str) -> None:
        self.execute()
        if self.cursor is not None and self.connection is not None:
            self.cursor.execute(sql)
            self.connection.commit()
        
        
    def query_one(self, sql: str) -> Optional[Any]:
        self.execute()
        if self.cursor is not None:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if result is None:
                return None
            else:
                return result
        else:
            return ''
        
    def query_list(self, sql: str) -> List:
        self.execute()
        if self.cursor is not None:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        else:
            return []
            