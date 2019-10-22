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

def backupDatabase():
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    DT_now = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())

    mycol = mydb["LDW"]
    data = mycol.find()
    with open(os.path.join(os.getcwd(), 'Database/backup_' + DT_now + '_LDW.json'), 'w') as f:
        for item in data:
            print(item)
            item.pop('_id')
            print(json.dumps(item, ensure_ascii=False, cls=CJsonEncoder))
            f.write(json.dumps(item, ensure_ascii=False, cls=CJsonEncoder))
            f.write('\n')

    mycol = mydb["MissingWrong"]
    data = mycol.find()
    with open(os.path.join(os.getcwd(), 'Database/backup_' + DT_now + '_MissingWrong.json'), 'w') as f:
        for item in data:
            print(item)
            item.pop('_id')
            print(json.dumps(item, ensure_ascii=False, cls=CJsonEncoder))
            f.write(json.dumps(item, ensure_ascii=False, cls=CJsonEncoder))
            f.write('\n')

