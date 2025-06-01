import taosws
from src.utils.logger import Logger
from src.config.configuration import DatabaseConfig, getDatabase

logger = Logger(__name__)


class Storage:
    def __init__(self) -> None:
        self.conn = None

    def __enter__(self):
        try:
            _dbc: DatabaseConfig = getDatabase()
            dsn: str = f"taosws://{_dbc.user}:{_dbc.password}@{_dbc.url}:{_dbc.port}"
            self.conn = taosws.connect(dsn)
            self.conn.execute(f"USE {_dbc.database}")
            return self
        except Exception:
            logger.error(f"数据库异常: {Exception}")

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.conn is not None:
            self.conn.close()

    def query(self, sql):
        return self.conn.query(sql)
