from unittest import TestCase
from service.table_service import Table1_Service, Table2_Service


class TestTable1Service(TestCase):

    def test_dist_table(self):
        service = Table1_Service()
        path: str = service.dist_table()


class TestTable2Service(TestCase):

    def test_dist_table(self):
        service = Table2_Service()
        path: str = service.dist_table()
