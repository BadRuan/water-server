from model import DatabaseConfig
from config.settings import DATABASE_DEV


def getDatabase() -> DatabaseConfig:
    return DATABASE_DEV
