from unittest import TestCase
from utils.logger import Logger
from dao.api_dao import ApiDao

logger = Logger(__name__)


class TestApiDao(TestCase):

    def test_select_all_count(self):
        dao = ApiDao()
        count: int = dao.select_all_count()
        logger.debug(f"测试查询语句，数据库共{count}条水位数据")

    def test_select_year_count(self):
        dao = ApiDao()
        count: int = dao.select_year_count()
        logger.debug(f"测试查询语句，数据库今年共{count}条水位数据")

    def test_select_every_stcd_count(self):
        dao = ApiDao()
        result = dao.select_every_stcd_count()

    def test_select_year_every_stcd_count(self):
        dao = ApiDao()
        count: int = dao.select_year_every_stcd_count()
