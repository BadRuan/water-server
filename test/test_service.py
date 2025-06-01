from src.service.table_service import Table1_Service, Table2_Service
from src.service.api_service import ApiService


class TestTableService:

    def test_dist_table(self):
        service1 = Table1_Service()
        service2 = Table2_Service()
        path1: str = service1.dist_table()
        path2: str = service2.dist_table()


class TestApiService:

    def test_getCountInfo(self):
        service = ApiService()
        total_count: int = service.getCountInfo().total_count
        assert total_count != 0

    def test_add_visit(self):
        service = ApiService()
        ip_address: str = "127.0.0.1"
        result: bool = service.add_visit(ip_address)
        assert result

    def test_add_download(self):
        service = ApiService()
        ip_address: str = "127.0.0.1"
        result: bool = service.add_download(ip_address)
        assert result
