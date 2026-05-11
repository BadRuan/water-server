from typing import List, Tuple
from enum import Enum
from src.model import DataConfig, Station


postgres: DataConfig = DataConfig(url='100.68.9.83', user='postgres', password='Deepseek666', port=54321, database='water') 

class COLOR(Enum):
    Default = "000000"
    SheFang = "189FA7"
    JingJie = "0070C0"
    BaoZheng = "FF0000"

STATIONS: List[Tuple[int, float, float, float, str]] = [
    (62904500, 11.5, 13.2, 15.84, "无为大堤"),
    (60115400, 9.4, 11.2, 13.4, "城北圩"),
    (62900700, 8.7, 10.7, 12.7, "江北（沈巷）长江堤"),
    (62906500, 10.1, 12.1, 14.1, "万春圈堤"),
    (62900700, 9.4, 11.2, 12.3, "裕溪口江堤"),
    (62900600, 9.5, 10.5, 12.0, "裕溪河堤"),
    (62905100, 8.5, 9.5, 11.5, "牛屯河堤"),
    (62904500, 11.5, 13.2, 14.5, "惠生连圩堤"),
    (62904500, 11.5, 13.2, 14.5, "永定大圩堤"),
    (62904500, 11.0, 13.0, 13.5, "黑沙洲、天然洲圩"),
]

station_list: List[Station] = [Station(code=s[0], name=s[4], sfsw=s[1], jjsw=s[2], bzsw=s[3]) for s in STATIONS]
