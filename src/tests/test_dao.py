from unittest import TestCase
from typing import List
from models.table import Station
from models.api_model import CountModel
from dao.table_dao import Table1_Dao, Table2_Dao
from dao.api_dao import ApiDao


class TestTable1Dao(TestCase):

    def test_get_table_data(self):
        dao = Table1_Dao()
        s: List[Station] = dao.get_table_data()
        self.assertIsNotNone(len(s))


class TestTable2Dao(TestCase):

    def test_get_table_data(self):
        dao = Table2_Dao()
        s: List[Station] = dao.get_table_data()
        self.assertIsNotNone(len(s))

class TestApiDao(TestCase):

    def test_getCountInfo(self):
        dao = ApiDao()
        c_info: CountModel = dao.getCountInfo()
