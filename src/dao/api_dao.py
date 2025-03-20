from typing import List
from models.api import ApiStation
from datetime import datetime
from utils.database_storage import DatabaseStorage
from datetime import datetime


class ApiDao:

    def select_all_count(self) -> int:
        SQL = f"SELECT COUNT(*) FROM waterlevel"
        with DatabaseStorage() as td:
            results = td.query(SQL)
            for r in results:
                return r[0]
            return 0

    def select_year_count(self) -> int:
        current_year: int = datetime.now().year
        SQL = f"SELECT COUNT(*) FROM `waterlevel` WHERE ts >= '{current_year}-01-01 00:00:00' AND ts < NOW()"
        with DatabaseStorage() as td:
            results = td.query(SQL)
            for r in results:
                return r[0]
            return 0

    def select_every_stcd_count(self) -> List[ApiStation]:
        SQL = f"SELECT `NAME`, count(*) FROM waterlevel GROUP BY `NAME`"
        with DatabaseStorage() as td:
            results = td.query(SQL)
            return [ApiStation(name=row[0], count=row[1]) for row in results]
        return []

    def select_year_every_stcd_count(self) -> List[ApiStation]:
        current_year: int = datetime.now().year
        SQL = f"SELECT `NAME`, count(*) FROM waterlevel WHERE ts >= '{current_year}-01-01 00:00:00' AND ts < NOW() GROUP BY `NAME`"
        with DatabaseStorage() as td:
            results = td.query(SQL)
            return [ApiStation(name=row[0], count=row[1]) for row in results]
        return []
