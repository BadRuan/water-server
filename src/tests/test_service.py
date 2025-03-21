from unittest import TestCase
from service.table_service import Table1_Service, Table2_Service
from service.api_service import ApiService
from utils.logger import Logger


logger = Logger(__name__)


class TestTable1Service(TestCase):

    def test_dist_table(self):
        service = Table1_Service()
        service.dist_table()


class TestTable2Service(TestCase):

    def test_dist_table(self):
        service = Table2_Service()
        service.dist_table()
        logger.debug("测试获取计数业务执行成功")


class TestApiService(TestCase):

    def test_getCountInfo(self):
        service = ApiService()
        service.getCountInfo()

    def test_add_visit(self):
        service = ApiService()
        ip_address: str = "127.0.0.1"
        service.add_visit(ip_address)
        logger.debug("测试增加浏览记录业务执行成功")

    def test_add_download(self):
        service = ApiService()
        ip_address: str = "127.0.0.1"
        service.add_download(ip_address)
        logger.debug("测试增加下载记录业务执行成功")
