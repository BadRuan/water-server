from models.api_model import CountModel
from dao.api_dao import ApiDao


class ApiService:
    def __init__(self):
        self.dao = ApiDao()

    def getCountInfo(self) -> CountModel:
        return self.dao.getCountInfo()

    def add_visit(self, ip_address: str) -> bool:
        return self.dao.add_recoder("website_access", ip_address)

    def add_download(self, ip_address: str) -> bool:
        return self.dao.add_recoder("table_downloads", ip_address)
