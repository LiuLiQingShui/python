import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pymongo
import base64
import time
import pytz
import json
import datetime


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
mydb = myclient["jimu_TestResult"]
LDW_database = r'backup_2019-10-22 10-23-17_LDW.json'
MissingWrong_database=r'backup_2019-10-22 10-23-17_MissingWrong.json'

mycol = mydb["LDW_restore"]
with open(os.path.join(os.getcwd(),'Database/'+LDW_database),'r') as f:
    data = f.readlines()
    for item in data:
        print(item)
        print(json.loads(item))
        mycol.insert_one(json.loads(item))


mycol = mydb["MissingWrong_restore"]
with open(os.path.join(os.getcwd(),'Database/'+MissingWrong_database),'r') as f:
    data = f.readlines()
    for item in data:
        print(item)
        print(json.loads(item))
        mycol.insert_one(json.loads(item))