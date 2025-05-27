from typing import List
from models.api_model import CountModel, StoryModel, RecentlyWaterModel
from datetime import datetime
from utils.storage import DatabaseStorage
from config.settings import RAW_STATIONS


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

    def query_recently(self) -> List[RecentlyWaterModel]:
        data_list: List[RecentlyWaterModel] = []
        with DatabaseStorage() as td:
            for station in RAW_STATIONS:
                query_sql: str = (
                    f"select TO_CHAR(ts, 'YYYY-mm-dd hh24:mi:ss'), `current` from `t{station.stcd}` ORDER BY `ts` DESC LIMIT 1"
                )
                r = td.query(query_sql)
                for r in r:
                    data_list.append(
                        RecentlyWaterModel(
                            name=station.name,
                            stcd=station.stcd,
                            current=round(r[1], 2),
                            tm=r[0],
                        )
                    )
        return data_list
