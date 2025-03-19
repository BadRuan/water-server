from unittest import TestSuite, TextTestRunner
from tests.test_configuration import TestConfiguration
from tests.test_storage import TestStorage
from tests.test_dao import TestTable1Dao, TestTable2Dao
from tests.test_service import TestTable1Service, TestTable2Service
from tests.test_apidao import TestApiDao


if __name__ == "__main__":
    suite = TestSuite()
    runner = TextTestRunner()

    case_list = [
        TestConfiguration("test_getDatabase"),
        TestStorage("test_connect"),
        TestStorage("test_query"),
        TestTable1Dao("test_get_table_data"),
        TestTable2Dao("test_get_table_data"),
        TestTable1Service("test_dist_table"),
        TestTable2Service("test_dist_table"),
        TestApiDao("test_select_all_count"),
        TestApiDao("test_select_year_count"),
        TestApiDao("test_select_every_stcd_count"),
        TestApiDao("test_select_year_every_stcd_count")
    ]

    suite.addTests(case_list)
    runner.run(suite)
