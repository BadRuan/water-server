from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    url: str
    port: int
    user: str
    password: str
    database: str
