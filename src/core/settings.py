from typing import List
from core.model import Database, Station


# 数据库参数
DATABASE_DEV = Database(
    url="tdengine", port=6041, user="root", password="123456", database="water"
)

STATIONS: List[Station] = [
    Station(stcd=62904500, sfsw=11.5, jjsw=13.2, bzsw=15.84, name="无为大堤"),
    Station(stcd=60115400, sfsw=9.4, jjsw=11.2, bzsw=13.4, name="城北圩"),
    Station(stcd=62900700, sfsw=8.7, jjsw=10.7, bzsw=12.7, name="江北（沈巷）长江堤"),
    Station(stcd=62906500, sfsw=10.1, jjsw=12.1, bzsw=14.1, name="万春圈堤"),
    Station(stcd=62900700, sfsw=9.4, jjsw=11.2, bzsw=12.3, name="裕溪口江堤"),
    Station(stcd=62900600, sfsw=9.5, jjsw=10.5, bzsw=12.0, name="裕溪河堤"),
    Station(stcd=62905100, sfsw=8.5, jjsw=9.5, bzsw=11.5, name="牛屯河堤"),
    Station(stcd=62904500, sfsw=11.5, jjsw=13.2, bzsw=14.5, name="惠生连圩堤"),
    Station(stcd=62904500, sfsw=11.5, jjsw=13.2, bzsw=15.84, name="永定大圩堤"),
    Station(stcd=62904500, sfsw=11.0, jjsw=13.0, bzsw=13.5, name="黑沙洲、天然洲圩"),
]
