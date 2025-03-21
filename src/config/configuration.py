from models.database import DatabaseConfig
from config.settings import DATABASE_TEST,DATABASE_DEV


def getDatabase() -> DatabaseConfig:
    return DATABASE_DEV
