from src.models.database import DatabaseConfig
from src.config.settings import DATABASE_DEV


def getDatabase() -> DatabaseConfig:
    return DATABASE_DEV
