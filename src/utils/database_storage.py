from utils.logger import Logger
import taosws
from config.configuration import DatabaseConfig, getDatabase

logger = Logger(__name__)


class DatabaseStorage:
    def __init__(self) -> None:
        self.conn = None
        self.initialized = False

    def init_connect(self):
        try:
            _dbc: DatabaseConfig = getDatabase()
            dsn = f"taosws://{_dbc.user}:{_dbc.password}@{_dbc.url}:{_dbc.port}"
            self.conn = taosws.connect(dsn)
            self.conn.execute(f"USE {_dbc.database}")
            logger.info("数据库已连接")
            self.initialized = True
        except Exception:
            logger.error(f"数据库异常: {Exception}")

    def ensure_initialized(self):
        if not self.initialized:
            self.init_connect()

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.conn is not None:
            self.conn.close()
            logger.info("数据库已断开")

    def __enter__(self):
        self.ensure_initialized()
        return self

    def query(self, sql):
        self.ensure_initialized()
        return self.conn.query(sql)
