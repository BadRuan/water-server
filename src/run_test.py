from unittest import TestSuite, TextTestRunner
from tests.test_configuration import TestConfiguration
from tests.test_storage import TestStorage
from tests.test_dao import TestTable1Dao, TestTable2Dao, TestApiDao
from tests.test_service import TestTable1Service, TestTable2Service, TestApiService


if __name__ == "__main__":
    suite = TestSuite()
    runner = TextTestRunner()

    case_list = [
        TestConfiguration("test_getDatabase"),
        TestStorage("test_connect"),
        TestStorage("test_query"),
        TestTable1Dao("test_get_table_data"),
        TestTable2Dao("test_get_table_data"),
        TestApiDao("test_getCountInfo"),
        TestTable1Service("test_dist_table"),
        TestTable2Service("test_dist_table"),
        TestApiService("test_getCountInfo"),
        TestApiService("test_add_visit"),
        TestApiService("test_add_download")
    ]

    suite.addTests(case_list)
    runner.run(suite)
