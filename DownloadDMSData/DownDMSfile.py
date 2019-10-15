import pymongo
import urllib.request
import time
import datetime
import csv
import os
import json

with open('configure.ini') as f:
   reader = csv.reader(f)
   content = list(reader)
   #print(content)
   alarmliststr = content[1][1:]
   alarmlist = []
   for item in alarmliststr:
      try:
         alarmlist.append(int(item))
      except:
         break
   print("alarm:",alarmlist)

   formatstr = content[2][1:]
   format = []
   for item in formatstr:
      try:
         format.append(int(item))
      except:
         break
   print("format:",format)

   # timestart = (time.mktime(time.strptime(content[0][1], "%Y-%m-%d %H:%M:%S")))
   # timestart = datetime.datetime.fromtimestamp(timestart)
   # timeend = (time.mktime(time.strptime(content[0][2], "%Y-%m-%d %H:%M:%S")))
   # timeend = datetime.datetime.fromtimestamp(timeend)
   timestart= datetime.datetime.strptime(content[0][1], "%Y-%m-%d %H:%M:%S")
   timeend = datetime.datetime.strptime(content[0][2], "%Y-%m-%d %H:%M:%S")
   print(timestart,timeend)

   myclient = pymongo.MongoClient('mongodb://47.110.225.26:27017/')
   mydb = myclient.jimu_db
   mydb.authenticate("export", "000000")
   mycol = mydb["alarm_resource"]

   myquery = {"alarmTime": {"$gte": timestart,"$lte":timeend},'format':{"$in":format},'alarm':{"$in":alarmlist}}

   DataFolder = os.path.join(os.getcwd(), 'Data')
   if not os.path.exists(DataFolder):
      os.makedirs(DataFolder)
   informationjson = os.path.join(DataFolder, 'information.json')
   with open(informationjson, 'w') as info_f:
      1
   mydoc = mycol.find(myquery)
   for item in mydoc:
      url = item['url']
      f = urllib.request.urlopen(url)
      with open(os.path.join(DataFolder, item['fileName']), "wb") as code:
         code.write(f.read())
      with open(informationjson,'a') as info_f:
         item.pop("_id")
         #print(item["alarmTime"])
         item["alarmTime"] = item["alarmTime"].strftime( '%Y-%m-%d %H:%M:%S %f' )
         item["uploadTime"] = item["uploadTime"].strftime('%Y-%m-%d %H:%M:%S %f')
         item["createAt"] = item["createAt"].strftime('%Y-%m-%d %H:%M:%S %f')
         #print(item["alarmTime"])
         print(item)
         print(json.dumps(item))
         info_f.write(json.dumps(item))
         info_f.write('\n')
      #print(x)





