from unittest import TestCase
from utils.storage import DatabaseStorage


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
                self.assertIsNotNone(r[0])
