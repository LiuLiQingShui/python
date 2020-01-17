import pymongo
import urllib.request
import time
import datetime
import csv
import os
import json
import pymysql
import shutil




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
   timeend = datetime.datetime.strptime(content[0][2], "%Y-%m-%d %H:%M:%S")
   print(content[0][1],content[0][2])
   print(timestart,timeend)

   #time.sleep(100000)

   exclude_DEVICE_ID=[]
   db = pymysql.connect('rm-bp1jzf2obq01ow7k9lo.mysql.rds.aliyuncs.com', 'jimu_read', 'jimu_db@Read', 'jimu_db')
   if len(excludecompany)>0:
      cursor = db.cursor()
      if len(excludecompany)>1:
         sql = 'SELECT ORG_ID FROM jimu_db.jmcl_org where ORG_NAME in ' + str(excludecompany)
      else:
         sql = 'SELECT ORG_ID FROM jimu_db.jmcl_org where ORG_NAME in ("' + str(excludecompany[0])+'")'
      print(sql)
      cursor.execute(sql)
      dat = cursor.fetchall()
      ID = ()
      for item in dat:
         ID = ID + item
      print(ID)
      if len(ID) > 0:
         if len(ID)>1:
            sql = 'SELECT DEVICE_ID FROM jimu_db.jmcl_device where ORG_ID in ' + str(ID)
         else:
            sql = 'SELECT DEVICE_ID FROM jimu_db.jmcl_device where ORG_ID in (' + str(ID[0])+')'
         print(sql)
         cursor.execute(sql)
         dat = cursor.fetchall()
         #print(dat)
         if len(dat)>0:
            for item in dat:
               exclude_DEVICE_ID.append(item[0])
   db.close()
   print(exclude_DEVICE_ID)
   # sql = '''
   # SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'jimu_db' AND TABLE_NAME = 'jmcl_org'
   # '''
   # cursor.execute(sql)
   # dat = cursor.fetchall()
   # print(list(dat))
   # print(type(dat))
   # COLLUMN_NAME = []
   # for item in dat:
   #    COLLUMN_NAME.append(item[0])
   # print(COLLUMN_NAME)

   #exclude_DEVICE_ID = []


   #time.sleep(1000000)

   myclient = pymongo.MongoClient('mongodb://47.110.225.26:27017/')
   mydb = myclient.jimu_db
   mydb.authenticate("export", "000000")
   mycol = mydb["alarm_resource"]

   myquery = {"alarmTime": {"$gte": timestart,"$lte":timeend},'format':{"$in":format},'alarm':{"$in":alarmlist},'deviceId':{'$in':exclude_DEVICE_ID}}
   print(myquery)
   #myquery = {"alarmTime": {"$gte": timestart, "$lte": timeend}, 'format': {"$in": format}, 'alarm': {"$in": alarmlist}}
   DataFolder = os.path.join(os.getcwd(), 'Data208')
   if os.path.exists(DataFolder):
       shutil.rmtree(DataFolder)
   os.makedirs(DataFolder)

   informationjson = os.path.join(DataFolder, 'information.json')
   with open(informationjson, 'w') as info_f:
      1
   mydoc = mycol.find(myquery)
   device={}
   for item in mydoc:
      #print(item)
      #datetime.datetime().hour 27 30
      #if item['alarmTime'].hour<=19 or item['alarmTime'].hour>=22:
         #continue
      #if time.localtime()
      # if item['deviceId'] in  device:
      #    if device[item['deviceId']] >=10:
      #       continue
      #    else:
      #       device[item['deviceId']] = device[item['deviceId']]+1
      # else:
      #    device[item['deviceId']] =  1
      url = item['url']
      try:
         f = urllib.request.urlopen(url,timeout=3)
         with open(os.path.join(DataFolder, item['fileName']), "wb") as code:
            code.write(f.read())
      except:
         print('failed!')
         continue

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





