from unittest import TestCase
from utils.database_storage import DatabaseStorage
from utils.logger import Logger

logger = Logger(__name__)


class TestStorage(TestCase):

    def test_connect(self):
        storage = DatabaseStorage()
        storage.init_connect()
        self.assertIsNotNone(storage.conn)

    def test_query(self):
        with DatabaseStorage() as storage:
            SQL = f"SELECT COUNT(*) FROM waterlevel"
            result = storage.query(SQL)
            self.assertIsNotNone(result)
            for r in result:
                logger.debug(f"执行查询语句，数据库共{r[0]}条水位数据")
