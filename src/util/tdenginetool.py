import taosws
from core.settings import DATABASE_DEV


class TDengineTool:
    def __init__(self) -> None:
        self.conn = None
        self.initialized = False

    def init_connect(self):
        try:
            c = DATABASE_DEV
            dsn = f"taosws://{c.user}:{c.password}@{c.url}:{c.port}/{c.database}"
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
