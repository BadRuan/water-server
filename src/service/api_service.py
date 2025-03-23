from typing import List
from models.api_model import CountModel, StoryModel, RecentlyWaterModel
from utils.logger import Logger
from dao.api_dao import ApiDao


logger = Logger(__name__)


class ApiService:
    def __init__(self):
        self.dao = ApiDao()

    def getCountInfo(self) -> CountModel:
        return self.dao.getCountInfo()

    def add_visit(self, ip_address: str) -> bool:
        logger.info(f"IP: {ip_address} 访问了本站")
        return self.dao.add_recoder("website_access", ip_address)

    def add_download(self, ip_address: str) -> bool:
        logger.info(f"IP {ip_address} 下载了水位表")
        return self.dao.add_recoder("table_downloads", ip_address)

    def get_story(self) -> List[StoryModel]:
        return self.dao.query_story()

    def get_recently(self) -> List[RecentlyWaterModel]:
        return self.dao.query_recently()
