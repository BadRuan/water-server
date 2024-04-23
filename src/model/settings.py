from pydantic import BaseModel


# 数据库参数格式
class Database(BaseModel):
    url: str
    port: int
    user: str
    password: str
    database: str


# 水文站参数格式
class Station(BaseModel):
    stcd: int
    name: str
