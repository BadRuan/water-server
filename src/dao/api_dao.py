from models.api_model import CountModel
from datetime import datetime
from utils.storage import DatabaseStorage


class ApiDao:

    def getCountInfo(self) -> CountModel:
        total_count: int = 0
        this_year_count: int = 0
        visit_count: int = 0
        download_count: int = 0

        total_count_SQL: str = f"SELECT COUNT(*) FROM waterlevel"
        current_year: int = datetime.now().year
        this_year_count_SQL: str = (
            f"SELECT COUNT(*) FROM `waterlevel` WHERE ts >= '{current_year}-01-01 00:00:00' AND ts < NOW()"
        )
        visit_count_SQL: str = f"SELECT count(*) FROM website_access"
        download_count_SQL: str = f"SELECT count(*) FROM table_downloads"

        with DatabaseStorage() as td:

            results = td.query(total_count_SQL)
            for r in results:
                total_count = r[0]
            results = td.query(this_year_count_SQL)
            for r in results:
                this_year_count = r[0]
            results = td.query(visit_count_SQL)
            for r in results:
                visit_count = r[0]
            results = td.query(download_count_SQL)
            for r in results:
                download_count = r[0]

        return CountModel(
            total_count=total_count,
            this_year_count=this_year_count,
            visit_count=visit_count,
            download_count=download_count,
        )

    def add_recoder(self, table_name: str, ip_address: str) -> bool:
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
        SQL: str = (
            f"INSERT INTO {table_name}  VALUES ('{formatted_date}.000', '{ip_address}')"
        )
        with DatabaseStorage() as td:
            td.query(SQL)
            return True
        return False
