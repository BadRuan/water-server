from model import ApiStation
from dao.api_dao import ApiDao

class ApiService:
    def __init__(self):
        self.dao = ApiDao()
    
    def getCountInfo(self):
        all_count: int = self.dao.select_all_count()
        year_count: int = self.dao.select_year_count()
        every_stcd_count: ApiStation = self.dao.select_every_stcd_count()
        year_every_stcd_count: ApiStation = self.dao.select_year_every_stcd_count()
        return {
            "all": all_count,
            "year": year_count,
            "station": every_stcd_count,
            "year_station": year_every_stcd_count
        }