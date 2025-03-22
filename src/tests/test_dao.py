from unittest import TestCase
from typing import List
from models.table import Station
from dao.table_dao import TableDao, Table1_Dao, Table2_Dao
from dao.api_dao import ApiDao


class TestTableDao(TestCase):

    def test_get_table_data(self):
        dao1: TableDao = Table1_Dao()
        dao2: TableDao = Table2_Dao()
        s1: List[Station] = dao1.get_table_data()
        s2: List[Station] = dao2.get_table_data()
        self.assertNotEqual(len(s1), 0)
        self.assertNotEqual(len(s2), 0)


class TestApiDao(TestCase):

    def test_getCountInfo(self):
        dao = ApiDao()
        total_count: int = dao.getCountInfo().total_count
        self.assertNotEqual(total_count, 0)
