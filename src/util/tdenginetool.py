import taosws
from config.settings import DATABASE_DEV


class TDengineTool:
    def __init__(self) -> None:
        self.conn = None
        self.initialized = False

    def init_connect(self):
        try:
            c = DATABASE_DEV
            dsn = f'taosws://{c.user}:{c.password}@{c.url}:{c.port}/{c.database}'
            self.conn = taosws.connect(dsn)
            self.initialized = True
        except BaseException as other:
            print("exception occur")
            print(other)

    def ensure_initialized(self):
        if not self.initialized:
            self.init_connect()

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.conn is not None:
            self.conn.close()

    def __enter__(self):
        self.ensure_initialized()
        return self.conn

    # 执行SQL语句
    async def execute_sql(self, sql: str) -> int:
        self.ensure_initialized()
        return self.conn.execute(sql)

    # 执行获取数据SQL语句
    async def query_fetch(self, sql):
        self.ensure_initialized()
        return self.conn.query(sql)
