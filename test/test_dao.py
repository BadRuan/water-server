from src.dao import DistTable_1, DistTable_2, DistTable_3, DistTable_4
from src.utils import Logger


log = Logger(__name__)

def test_dist_table_1():
    DistTable_1().dist()
    DistTable_2().dist()
    DistTable_3().dist()
    DistTable_4().dist()