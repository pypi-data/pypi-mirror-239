# -*- coding:utf-8 -*-

# LOCAL_DATA_PATH= r"K:\cscfut\data\sample_data"
import os

if os.name == 'nt':
    LOCAL_DATA_PATH = r"K:\qtData\cscdata_repo"
elif os.name == 'posix':
    LOCAL_DATA_PATH = r"/mnt/k/qtData/cscdata_repo"
else:
    raise Exception('Unknown os.name: {}'.format(os.name))

USERDB_LIST= [
    'wp',
    'gjl',
    'rtt',
    'wcc',
    'fyq',
    'xhn',
    'rp'

]
DATABASE_LIST =[
    'intraday_data',
    'cnfut',
    'cnstk'
]


