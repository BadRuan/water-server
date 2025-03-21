from models.database import DatabaseConfig
from config.settings import DATABASE_TEST


def getDatabase() -> DatabaseConfig:
    return DATABASE_TEST
