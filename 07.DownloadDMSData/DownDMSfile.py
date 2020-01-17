import pymongo
import urllib.request
import time
import datetime
import csv
import os
import json
import pymysql
import pytz


with open('configure.ini',encoding='utf-8') as f:
   reader = csv.reader(f)
   content = list(reader)
   print(content)
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

   excludecompanystr = content[3][1:]
   excludecompany = ()
   for item in excludecompanystr:
      try:
         print(item)
         if item!='':
            print(item)
            excludecompany = excludecompany+tuple([item])
      except:
         break
   print('exclude company:',excludecompany)
   timestart= datetime.datetime.strptime(content[0][1], "%Y-%m-%d %H:%M:%S")
   timestart = timestart.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
   timestart = timestart.astimezone(tz=pytz.timezone('UTC'))
   #print(timestart.tzname())

   #print(timestart)
   timeend = datetime.datetime.strptime(content[0][2], "%Y-%m-%d %H:%M:%S")
   timeend = timeend.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
   timeend = timeend.astimezone(tz=pytz.timezone('UTC'))
   print(timestart,timeend)


   #time.sleep(6000)

   exclude_DEVICE_ID=[]
   db = pymysql.connect('rm-bp1jzf2obq01ow7k9lo.mysql.rds.aliyuncs.com', 'jimu_read', 'jimu_db@Read', 'jimu_db')
   if len(excludecompany)>0:
      cursor = db.cursor()
      sql = 'SELECT ORG_ID FROM jimu_db.jmcl_org where ORG_NAME in ' + str(excludecompany)
      print(sql)
      cursor.execute(sql)
      dat = cursor.fetchall()
      ID = ()
      for item in dat:
         ID = ID + item
      print(ID)
      if len(ID) > 0:
         sql = 'SELECT DEVICE_ID FROM jimu_db.jmcl_device where ORG_ID in ' + str(ID)
         print(sql)
         cursor.execute(sql)
         dat = cursor.fetchall()
         if len(dat)>0:
            for item in dat:
               exclude_DEVICE_ID.append(item[0])
   db.close()
   print(exclude_DEVICE_ID)
   myclient = pymongo.MongoClient('mongodb://47.110.225.26:27017/')
   mydb = myclient.jimu_db
   mydb.authenticate("export", "000000")
   mycol = mydb["alarm_resource"]

   myquery = {"alarmTime": {"$gte": timestart,"$lte":timeend},'format':{"$in":format},'alarm':{"$in":alarmlist},'deviceId':{'$nin':exclude_DEVICE_ID}}
   DataFolder = os.path.join(os.getcwd(), 'Data')
   if not os.path.exists(DataFolder):
      os.makedirs(DataFolder)
   informationjson = os.path.join(DataFolder, 'information.json')
   with open(informationjson, 'w') as info_f:
      1
   mydoc = mycol.find(myquery)
   device={}
   count = 1
   for item in mydoc:
      print(item)
      url = item['url']

      #timeend = timeend.astimezone(tz=pytz.timezone('UTC'))
      #replace(tzinfo=pytz.timezone('Asia/Shanghai'))
      item["alarmTime"] = item["alarmTime"].replace(tzinfo=pytz.timezone('UTC'))
      item["alarmTime"] = item["alarmTime"].astimezone(tz=pytz.timezone('Asia/Shanghai'))
      item["uploadTime"] = item["uploadTime"].replace(tzinfo=pytz.timezone('UTC'))
      item["uploadTime"] = item["uploadTime"].astimezone(tz=pytz.timezone('Asia/Shanghai'))
      item["createAt"] = item["createAt"].replace(tzinfo=pytz.timezone('UTC'))
      item["createAt"] = item["createAt"].astimezone(tz=pytz.timezone('Asia/Shanghai'))
      print(item["alarmTime"].tzname())
      try:
         f = urllib.request.urlopen(url,timeout=3)
         with open(os.path.join(DataFolder, str(item['alarm'])+'__'+'{:06}'.format(count)+'__'+item["alarmTime"].strftime( '%Y-%m-%d__%H-%M-%S')+'__'+item['fileName']), "wb") as code:
            code.write(f.read())
         count = count +1
      except:
         print('failed!')
         continue
      with open(informationjson,'a') as info_f:
         item.pop("_id")
         item["alarmTime"] = item["alarmTime"].strftime( '%Y-%m-%d %H:%M:%S %f' )
         item["uploadTime"] = item["uploadTime"].strftime('%Y-%m-%d %H:%M:%S %f')
         item["createAt"] = item["createAt"].strftime('%Y-%m-%d %H:%M:%S %f')
         print(item)
         print(json.dumps(item))
         info_f.write(json.dumps(item))
         info_f.write('\n')





