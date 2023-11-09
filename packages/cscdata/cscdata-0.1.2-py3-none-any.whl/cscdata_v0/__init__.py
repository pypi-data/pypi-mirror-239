# -*- coding:utf-8 -*-

from .config import LOCAL_DATA_PATH, USERDB_LIST, DATABASE_LIST
import os

def init(path):
    """提供给外部测试数据源的init方法"""

    global LOCAL_DATA_PATH, USERDB_LIST, DATABASE_LIST

    LOCAL_DATA_PATH = path

    USERDB_LIST = [i for i in os.listdir(path)]

    DATABASE_LIST = [i for i in os.listdir(path)]

# here assert some global params
_TRADE_DTS = []
...

def initialize(trade_dts):
    """initialize some params support table function"""
    global _TRADE_DTS

    _TRADE_DTS = trade_dts

from .localAbstract import *

DB_ENGINE_SUPPORT = [
    "h5",
    "parquet",
    "others"
]

PARQUET_TABLE_SUPPORT = [
    "file",
    "directory",
]
H5_TABLE_SUPPORT = [

]