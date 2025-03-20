from models.api import DataModel
from dao.api_dao import ApiDao


class ApiService:
    def __init__(self):
        self.dao = ApiDao()

    def getCountInfo(self) -> DataModel:
        return DataModel(
            total_count=self.dao.select_all_count(),
            this_year_count=self.dao.select_year_count(),
            count_by_station=self.dao.select_every_stcd_count(),
            this_year_count_by_station=self.dao.select_year_every_stcd_count(),
        )
