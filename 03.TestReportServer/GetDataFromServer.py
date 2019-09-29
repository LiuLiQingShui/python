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

def imageToStr(image):
    with open(image,'rb') as f:
        image_byte=base64.b64encode(f.read())
    image_str=image_byte.decode('ascii') #byte类型转换为str
    return image_str


def getSummary():
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]
    Summarylist = []
    data = mycol.find()
    for item in data:
        if 'OrangeBinData' in item:
            Summarylist.append([item['OrangeBinData'],item['Time'],item['Timestamp']])
    print(Summarylist)
    if len(Summarylist)==0:
        return {}
    else:
        return {"Data":Summarylist}


def getsummarymissingwrong():
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["MissingWrong"]
    Summarylist = []
    data = mycol.find()
    for item in data:
        if 'ID' in item:
            Summarylist.append([item['ID'],item['Time'],item['Timestamp']])
    print(Summarylist)
    if len(Summarylist)==0:
        return {}
    else:
        return {"Data":Summarylist}


def getversion(type):
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb[type]
    Summarylist = []
    data = mycol.find()
    for item in data:
        if 'version' in item:
            Summarylist.append(item['version'])
    Summarylist=list(set(Summarylist))
    Summarylist.sort()
    print(Summarylist)
    if len(Summarylist)==0:
        return {}
    else:
        return {"Data":Summarylist}


def deleteoneitem(filename):
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]
    myquery = {"OrangeBinData": filename}
    mycol.delete_one(myquery)
    return {}
    #data = mycol.find_one(myquery)


def deleteoneitemmissingwrong(filename):
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["MissingWrong"]
    myquery = {"ID": filename}
    mycol.delete_one(myquery)
    return {}

def getOneItem(filename):
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]
    myquery = {"OrangeBinData": {"$regex":filename}}
    data = mycol.find_one(myquery)
    if not data:
        return {}
    # valueGeted=[]
    # for item in data:
    #     valueGeted.append(item)
    #     break
    data.pop("_id")
    LDW = (np.array(data['LDW'])).astype(np.float)
    T = [LDW[:,0]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))]),LDW[:,1]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))]),LDW[:,2]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))])]
    for i in range(len(T)):
        LDW = np.insert(LDW,len(LDW[0,:]), values=T[i], axis=1)
    TTC = (np.array(data['TTC'])).astype(np.float)
    T = [TTC[:,0]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))]),TTC[:,1]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))]),TTC[:,2]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))])]
    for i in range(len(T)):
        TTC = np.insert(TTC,len(TTC[0,:]), values=T[i], axis=1)

    LDW = np.nan_to_num(LDW)  # 替换nan为0.否则json接口查询会出错
    TTC = np.nan_to_num(TTC)
    data['LDW'] = LDW.tolist()
    data['TTC'] = TTC.tolist()
    print(data)
    # LDW = pd.DataFrame(LDW,
    #                    index=['Mobileye LDW左', 'Jimu LDW左', 'Mobileye LDW右', 'Jimu LDW右', 'Mobileye Total',
    #                           'Jimu Total'], columns=['Right', 'Missing', 'Wrong','Right_ratio','Missing_ratio','Wrong_ratio'])
    # plt.close('all')
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # LDW.iloc[:, :3].plot.bar(stacked=True, figsize=(8, 8),
    #                          title='LDW告警对比分析：Jimu、Mobileye\n' + data['Time'])
    # [(plt.text(k * 2 + 1, (LDW.iloc[1::2, :3].to_numpy())[k, 0], '%d' % (LDW.iloc[1::2, :3].to_numpy())[k, 0],
    #            ha='center', va='top'),
    #   plt.text(k * 2 + 1, (LDW.iloc[1::2, :3].to_numpy())[k, :2].sum(), '%d' % (LDW.iloc[1::2, :3].to_numpy())[k, 1],
    #            ha='center', va='top'),
    #   plt.text(k * 2 + 1, (LDW.iloc[1::2, :3].to_numpy())[k, :3].sum(), '%d' % (LDW.iloc[1::2, :3].to_numpy())[k, 2],
    #            ha='center', va='top')) for k in range(len(LDW.iloc[1::2, 2].to_numpy()))]
    # [(plt.text(k * 2, (LDW.iloc[0::2, :3].to_numpy())[k, 0], '%d' % (LDW.iloc[0::2, :3].to_numpy())[k, 0], ha='center',
    #            va='top')) for k in range(len(LDW.iloc[0::2, 2].to_numpy()))]
    # plt.xticks(rotation=30)
    # plt.savefig('LDW.png')
    # plt.close()
    # image = imageToStr('LDW.png')
    #data['LDW_bar'] = image

    # TTC = pd.DataFrame(TTC,
    #                    index=['TTC_Mobileye','TTC_Jimu'], columns=['Right', 'Missing', 'Wrong','Right_ratio','Missing_ratio','Wrong_ratio'])
    #
    # TTC.iloc[:, :3].plot.bar(stacked=True, figsize=(8, 8),
    #                          title='TTC告警对比分析：Jimu、Mobileye\n' + data['Time'])
    # [(plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, 0], '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 0],
    #            ha='center', va='top'),
    #   plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, :2].sum(), '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 1],
    #            ha='center', va='top'),
    #   plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, :3].sum(), '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 2],
    #            ha='center', va='top')) for k in range(len(TTC.iloc[1::2, 2].to_numpy()))]
    # [(plt.text(k * 2, (TTC.iloc[0::2, :3].to_numpy())[k, 0], '%d' % (TTC.iloc[0::2, :3].to_numpy())[k, 0], ha='center',
    #            va='top')) for k in range(len(TTC.iloc[0::2, 2].to_numpy()))]
    # plt.xticks(rotation=30)
    # plt.savefig('TTC.png')
    # plt.close()
    # image = imageToStr('TTC.png')
    #data['TTC_bar'] = image

    return data


def getOneItemmissingwrong(filename):
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["MissingWrong"]
    myquery = {"ID": filename}
    data = mycol.find_one(myquery)
    if not data:
        return {}
    data.pop("_id")
    return data



def getDataByTime(starttime,endtime,Situation):
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]
    dbdata = mycol.find()
    if not dbdata:
        return []
    # valueGeted=[]
    # for item in data:
    #     valueGeted.append(item)
    #     break
    cst_tz = pytz.timezone('Asia/Shanghai')
    utc_tz = pytz.timezone('UTC')
    count = 0



    #print(Situation)
    for item in dbdata:
        if Situation==140:
            1
        elif len(Situation)>0:
            dict = {}
            # dict['光照'] = 1
            for x in Situation:
                t = x.split("-")
                if t[0] not in dict:
                    dict[t[0]] = [t[1]]
                else:
                    attt = dict[t[0]]
                    attt.append(t[1])
                    dict[t[0]] = attt
            if 'Situation' in item:
                findlaber = 1
                for key, value in dict.items():
                    findlaber_sub = 0
                    for t in value:
                        if (key + '-' + t) in item['Situation']:
                            findlaber_sub = 1
                            break;
                    if findlaber_sub == 0:
                        findlaber = 0
                        break
                if findlaber==0:
                    continue
            else:
                continue
        else:
            continue



        if item['Timestamp'][0]>=starttime and item['Timestamp'][0]<=endtime:
            print(item['OrangeBinData'])
            if count>0:
                LDW = LDW + (np.array(item['LDW'])).astype(np.float)
                TTC = TTC + (np.array(item['TTC'])).astype(np.float)
                LDW_specific = LDW_specific + [
                    [(ts[0].replace(tzinfo=utc_tz)).astimezone(cst_tz).strftime('%y-%m-%d %H:%M:%S ')] + ts[1:] for ts
                    in item['LDW_specific']]
                TTC_specific = TTC_specific + [
                    [(ts[0].replace(tzinfo=utc_tz)).astimezone(cst_tz).strftime('%y-%m-%d %H:%M:%S ')] + ts[1:] for ts
                    in item['TTC_specific']]
            else:
                LDW = (np.array(item['LDW'])).astype(np.float)
                TTC = (np.array(item['TTC'])).astype(np.float)
                LDW_specific = [
                    [(ts[0].replace(tzinfo=utc_tz)).astimezone(cst_tz).strftime('%y-%m-%d %H:%M:%S ')] + ts[1:] for ts
                    in item['LDW_specific']]
                TTC_specific = [
                    [(ts[0].replace(tzinfo=utc_tz)).astimezone(cst_tz).strftime('%y-%m-%d %H:%M:%S ')] + ts[1:] for ts
                    in item['TTC_specific']]
            count = count + 1

    if count==0:
        return {}

    print(LDW)
    print(TTC)
    print(LDW_specific)
    print(TTC_specific)
    data = {}

    #LDW = (np.array(data['LDW'])).astype(np.float)
    T = [LDW[:,0]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))]),LDW[:,1]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))]),LDW[:,2]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))])]
    for i in range(len(T)):
        LDW = np.insert(LDW,len(LDW[0,:]), values=T[i], axis=1)
    #TTC = (np.array(data['TTC'])).astype(np.float)
    T = [TTC[:,0]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))]),TTC[:,1]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))]),TTC[:,2]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))])]
    for i in range(len(T)):
        TTC = np.insert(TTC,len(TTC[0,:]), values=T[i], axis=1)

    LDW = np.nan_to_num(LDW)#替换nan为0.否则json接口查询会出错
    TTC = np.nan_to_num(TTC)
    data['LDW'] = LDW.tolist()
    data['TTC'] = TTC.tolist()
    print(data)
    LDW = pd.DataFrame(LDW,
                       index=['Mobileye LDW左', 'Jimu LDW左', 'Mobileye LDW右', 'Jimu LDW右', 'Mobileye Total',
                              'Jimu Total'], columns=['Right', 'Missing', 'Wrong','Right_ratio','Missing_ratio','Wrong_ratio'])
    plt.close('all')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    LDW.iloc[:, :3].plot.bar(stacked=True, figsize=(8, 8),
                             title='LDW告警对比分析：Jimu、Mobileye\n' )
    [(plt.text(k * 2 + 1, (LDW.iloc[1::2, :3].to_numpy())[k, 0], '%d' % (LDW.iloc[1::2, :3].to_numpy())[k, 0],
               ha='center', va='top'),
      plt.text(k * 2 + 1, (LDW.iloc[1::2, :3].to_numpy())[k, :2].sum(), '%d' % (LDW.iloc[1::2, :3].to_numpy())[k, 1],
               ha='center', va='top'),
      plt.text(k * 2 + 1, (LDW.iloc[1::2, :3].to_numpy())[k, :3].sum(), '%d' % (LDW.iloc[1::2, :3].to_numpy())[k, 2],
               ha='center', va='top')) for k in range(len(LDW.iloc[1::2, 2].to_numpy()))]
    [(plt.text(k * 2, (LDW.iloc[0::2, :3].to_numpy())[k, 0], '%d' % (LDW.iloc[0::2, :3].to_numpy())[k, 0], ha='center',
               va='top')) for k in range(len(LDW.iloc[0::2, 2].to_numpy()))]
    plt.xticks(rotation=30)
    plt.savefig('LDW.png')
    plt.close()
    image = imageToStr('LDW.png')
    data['LDW_bar'] = image

    TTC = pd.DataFrame(TTC,
                       index=['TTC_Mobileye','TTC_Jimu'], columns=['Right', 'Missing', 'Wrong','Right_ratio','Missing_ratio','Wrong_ratio'])

    TTC.iloc[:, :3].plot.bar(stacked=True, figsize=(8, 8),
                             title='TTC告警对比分析：Jimu、Mobileye\n'  )
    [(plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, 0], '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 0],
               ha='center', va='top'),
      plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, :2].sum(), '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 1],
               ha='center', va='top'),
      plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, :3].sum(), '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 2],
               ha='center', va='top')) for k in range(len(TTC.iloc[1::2, 2].to_numpy()))]
    [(plt.text(k * 2, (TTC.iloc[0::2, :3].to_numpy())[k, 0], '%d' % (TTC.iloc[0::2, :3].to_numpy())[k, 0], ha='center',
               va='top')) for k in range(len(TTC.iloc[0::2, 2].to_numpy()))]
    plt.xticks(rotation=30)
    plt.savefig('TTC.png')
    plt.close()
    image = imageToStr('TTC.png')
    data['TTC_bar'] = image
    data['LDW_specific']=LDW_specific
    data['TTC_specific']=TTC_specific
    return data


def getdatabyversion(version,Situation):
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]
    dbdata = mycol.find()
    if not dbdata:
        return []
    # valueGeted=[]
    # for item in data:
    #     valueGeted.append(item)
    #     break
    cst_tz = pytz.timezone('Asia/Shanghai')
    utc_tz = pytz.timezone('UTC')
    count = 0



    #print(Situation)
    for item in dbdata:
        if Situation==140:
            1
            #print("AAAA")
        elif len(Situation)>0:
            dict = {}
            # dict['光照'] = 1
            for x in Situation:
                t = x.split("-")
                if t[0] not in dict:
                    dict[t[0]] = [t[1]]
                else:
                    attt = dict[t[0]]
                    attt.append(t[1])
                    dict[t[0]] = attt
            if 'Situation' in item:
                findlaber = 1
                for key, value in dict.items():
                    findlaber_sub = 0
                    for t in value:
                        if (key + '-' + t) in item['Situation']:
                            findlaber_sub = 1
                            break;
                    if findlaber_sub == 0:
                        findlaber = 0
                        break
                if findlaber==0:
                    continue
            else:
                continue
        else:
            continue


        if item['version']==version:
            if count>0:
                LDW = LDW + (np.array(item['LDW'])).astype(np.float)
                TTC = TTC + (np.array(item['TTC'])).astype(np.float)
            else:
                LDW = (np.array(item['LDW'])).astype(np.float)
                TTC = (np.array(item['TTC'])).astype(np.float)
            count = count + 1

    if count==0:
        return {}

    data = {}

    #LDW = (np.array(data['LDW'])).astype(np.float)
    T = [LDW[:,0]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))]),LDW[:,1]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))]),LDW[:,2]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))])]
    for i in range(len(T)):
        LDW = np.insert(LDW,len(LDW[0,:]), values=T[i], axis=1)
    #TTC = (np.array(data['TTC'])).astype(np.float)
    T = [TTC[:,0]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))]),TTC[:,1]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))]),TTC[:,2]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))])]
    for i in range(len(T)):
        TTC = np.insert(TTC,len(TTC[0,:]), values=T[i], axis=1)

    LDW = np.nan_to_num(LDW)#替换nan为0.否则json接口查询会出错
    TTC = np.nan_to_num(TTC)
    data['LDW'] = LDW.tolist()
    data['TTC'] = TTC.tolist()
    print(data)
    return data

def getdatabyversion_bac(version,Situation):
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]
    dbdata = mycol.find()
    if not dbdata:
        return []
    # valueGeted=[]
    # for item in data:
    #     valueGeted.append(item)
    #     break
    cst_tz = pytz.timezone('Asia/Shanghai')
    utc_tz = pytz.timezone('UTC')
    count = 0



    #print(Situation)
    for item in dbdata:
        if Situation is not None and len(Situation)>0:
            dict = {}
            # dict['光照'] = 1
            for x in Situation:
                t = x.split("-")
                if t[0] not in dict:
                    dict[t[0]] = [t[1]]
                else:
                    attt = dict[t[0]]
                    attt.append(t[1])
                    dict[t[0]] = attt
            if 'Situation' in item:
                findlaber = 1
                for key, value in dict.items():
                    findlaber_sub = 0
                    for t in value:
                        if (key + '-' + t) in item['Situation']:
                            findlaber_sub = 1
                            break;
                    if findlaber_sub == 0:
                        findlaber = 0
                        break
                if findlaber==0:
                    continue
            else:
                continue



        if item['version']==version:
            if count>0:
                LDW = LDW + (np.array(item['LDW'])).astype(np.float)
                TTC = TTC + (np.array(item['TTC'])).astype(np.float)
                LDW_specific = LDW_specific + [
                    [(ts[0].replace(tzinfo=utc_tz)).astimezone(cst_tz).strftime('%y-%m-%d %H:%M:%S ')] + ts[1:] for ts
                    in item['LDW_specific']]
                TTC_specific = TTC_specific + [
                    [(ts[0].replace(tzinfo=utc_tz)).astimezone(cst_tz).strftime('%y-%m-%d %H:%M:%S ')] + ts[1:] for ts
                    in item['TTC_specific']]
            else:
                LDW = (np.array(item['LDW'])).astype(np.float)
                TTC = (np.array(item['TTC'])).astype(np.float)
                LDW_specific = [
                    [(ts[0].replace(tzinfo=utc_tz)).astimezone(cst_tz).strftime('%y-%m-%d %H:%M:%S ')] + ts[1:] for ts
                    in item['LDW_specific']]
                TTC_specific = [
                    [(ts[0].replace(tzinfo=utc_tz)).astimezone(cst_tz).strftime('%y-%m-%d %H:%M:%S ')] + ts[1:] for ts
                    in item['TTC_specific']]
            count = count + 1

    if count==0:
        return {}

    print(LDW)
    print(TTC)
    print(LDW_specific)
    print(TTC_specific)
    data = {}

    #LDW = (np.array(data['LDW'])).astype(np.float)
    T = [LDW[:,0]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))]),LDW[:,1]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))]),LDW[:,2]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))])]
    for i in range(len(T)):
        LDW = np.insert(LDW,len(LDW[0,:]), values=T[i], axis=1)
    #TTC = (np.array(data['TTC'])).astype(np.float)
    T = [TTC[:,0]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))]),TTC[:,1]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))]),TTC[:,2]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))])]
    for i in range(len(T)):
        TTC = np.insert(TTC,len(TTC[0,:]), values=T[i], axis=1)

    LDW = np.nan_to_num(LDW)#替换nan为0.否则json接口查询会出错
    TTC = np.nan_to_num(TTC)
    data['LDW'] = LDW.tolist()
    data['TTC'] = TTC.tolist()
    print(data)
    LDW = pd.DataFrame(LDW,
                       index=['Mobileye LDW左', 'Jimu LDW左', 'Mobileye LDW右', 'Jimu LDW右', 'Mobileye Total',
                              'Jimu Total'], columns=['Right', 'Missing', 'Wrong','Right_ratio','Missing_ratio','Wrong_ratio'])
    plt.close('all')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    LDW.iloc[:, :3].plot.bar(stacked=True, figsize=(8, 8),
                             title='LDW告警对比分析：Jimu、Mobileye\n' )
    [(plt.text(k * 2 + 1, (LDW.iloc[1::2, :3].to_numpy())[k, 0], '%d' % (LDW.iloc[1::2, :3].to_numpy())[k, 0],
               ha='center', va='top'),
      plt.text(k * 2 + 1, (LDW.iloc[1::2, :3].to_numpy())[k, :2].sum(), '%d' % (LDW.iloc[1::2, :3].to_numpy())[k, 1],
               ha='center', va='top'),
      plt.text(k * 2 + 1, (LDW.iloc[1::2, :3].to_numpy())[k, :3].sum(), '%d' % (LDW.iloc[1::2, :3].to_numpy())[k, 2],
               ha='center', va='top')) for k in range(len(LDW.iloc[1::2, 2].to_numpy()))]
    [(plt.text(k * 2, (LDW.iloc[0::2, :3].to_numpy())[k, 0], '%d' % (LDW.iloc[0::2, :3].to_numpy())[k, 0], ha='center',
               va='top')) for k in range(len(LDW.iloc[0::2, 2].to_numpy()))]
    plt.xticks(rotation=30)
    plt.savefig('LDW.png')
    plt.close()
    image = imageToStr('LDW.png')
    data['LDW_bar'] = image

    TTC = pd.DataFrame(TTC,
                       index=['TTC_Mobileye','TTC_Jimu'], columns=['Right', 'Missing', 'Wrong','Right_ratio','Missing_ratio','Wrong_ratio'])

    TTC.iloc[:, :3].plot.bar(stacked=True, figsize=(8, 8),
                             title='TTC告警对比分析：Jimu、Mobileye\n'  )
    [(plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, 0], '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 0],
               ha='center', va='top'),
      plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, :2].sum(), '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 1],
               ha='center', va='top'),
      plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, :3].sum(), '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 2],
               ha='center', va='top')) for k in range(len(TTC.iloc[1::2, 2].to_numpy()))]
    [(plt.text(k * 2, (TTC.iloc[0::2, :3].to_numpy())[k, 0], '%d' % (TTC.iloc[0::2, :3].to_numpy())[k, 0], ha='center',
               va='top')) for k in range(len(TTC.iloc[0::2, 2].to_numpy()))]
    plt.xticks(rotation=30)
    plt.savefig('TTC.png')
    plt.close()
    image = imageToStr('TTC.png')
    data['TTC_bar'] = image
    data['LDW_specific']=LDW_specific
    data['TTC_specific']=TTC_specific
    return data

def getDataByTimemissingwrong(starttime,endtime,Situation):
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["MissingWrong"]
    dbdata = mycol.find()
    if not dbdata:
        return []
    # valueGeted=[]
    # for item in data:
    #     valueGeted.append(item)
    #     break
    cst_tz = pytz.timezone('Asia/Shanghai')
    utc_tz = pytz.timezone('UTC')
    count = 0



    #print(Situation)
    for item in dbdata:
        if Situation==140:
            1
        elif len(Situation)>0:
            dict = {}
            # dict['光照'] = 1
            for x in Situation:
                t = x.split("-")
                if t[0] not in dict:
                    dict[t[0]] = [t[1]]
                else:
                    attt = dict[t[0]]
                    attt.append(t[1])
                    dict[t[0]] = attt
            if 'Situation' in item:
                findlaber = 1
                for key, value in dict.items():
                    findlaber_sub = 0
                    for t in value:
                        if (key + '-' + t) in item['Situation']:
                            findlaber_sub = 1
                            break;
                    if findlaber_sub == 0:
                        findlaber = 0
                        break
                if findlaber==0:
                    continue
            else:
                continue
        else:
            continue


        if item['Timestamp'][0]>=starttime and item['Timestamp'][0]<=endtime:
            if count>0:
                distance = distance + (np.array(item['distance'])).astype(np.float)
                Car_wrong = Car_wrong + (np.array(item['Car_wrong'])).astype(np.float)
                Car_missing = Car_missing + (np.array(item['Car_missing'])).astype(np.float)
                persion_wrong = persion_wrong + (np.array(item['persion_wrong'])).astype(np.float)
                persion_missing = persion_missing + (np.array(item['persion_missing'])).astype(np.float)
            else:
                distance = (np.array(item['distance'])).astype(np.float)
                Car_wrong =  (np.array(item['Car_wrong'])).astype(np.float)
                Car_missing = (np.array(item['Car_missing'])).astype(np.float)
                persion_wrong = (np.array(item['persion_wrong'])).astype(np.float)
                persion_missing =  (np.array(item['persion_missing'])).astype(np.float)
            count = count + 1
    if count==0:
        distance = 0
        Car_wrong = 0
        Car_missing = 0
        persion_wrong = 0
        persion_missing = 0
    else:
        distance = distance.tolist()
        Car_wrong = Car_wrong.tolist()
        Car_missing = Car_missing.tolist()
        persion_wrong = persion_wrong.tolist()
        persion_missing = persion_missing.tolist()
    data = {'distance':distance,'Car_wrong':Car_wrong,'Car_missing':Car_missing,'persion_wrong':persion_wrong,'persion_missing':persion_missing}
    return data




def getdatabyversionmissingwrong(version,Situation):
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["MissingWrong"]
    dbdata = mycol.find()
    if not dbdata:
        return []
    # valueGeted=[]
    # for item in data:
    #     valueGeted.append(item)
    #     break
    cst_tz = pytz.timezone('Asia/Shanghai')
    utc_tz = pytz.timezone('UTC')
    count = 0



    #print(Situation)
    for item in dbdata:
        if Situation==140:
            1
        elif len(Situation)>0:
            dict = {}
            # dict['光照'] = 1
            for x in Situation:
                t = x.split("-")
                if t[0] not in dict:
                    dict[t[0]] = [t[1]]
                else:
                    attt = dict[t[0]]
                    attt.append(t[1])
                    dict[t[0]] = attt
            if 'Situation' in item:
                findlaber = 1
                for key, value in dict.items():
                    findlaber_sub = 0
                    for t in value:
                        if (key + '-' + t) in item['Situation']:
                            findlaber_sub = 1
                            break;
                    if findlaber_sub == 0:
                        findlaber = 0
                        break
                if findlaber==0:
                    continue
            else:
                continue
        else:
            continue



        if item['version']==version:
            if count>0:
                distance = distance + (np.array(item['distance'])).astype(np.float)
                Car_wrong = Car_wrong + (np.array(item['Car_wrong'])).astype(np.float)
                Car_missing = Car_missing + (np.array(item['Car_missing'])).astype(np.float)
                persion_wrong = persion_wrong + (np.array(item['persion_wrong'])).astype(np.float)
                persion_missing = persion_missing + (np.array(item['persion_missing'])).astype(np.float)
            else:
                distance = (np.array(item['distance'])).astype(np.float)
                Car_wrong =  (np.array(item['Car_wrong'])).astype(np.float)
                Car_missing = (np.array(item['Car_missing'])).astype(np.float)
                persion_wrong = (np.array(item['persion_wrong'])).astype(np.float)
                persion_missing =  (np.array(item['persion_missing'])).astype(np.float)
            count = count + 1
    if count==0:
        distance = 0
        Car_wrong = 0
        Car_missing = 0
        persion_wrong = 0
        persion_missing = 0
    else:
        distance = distance.tolist()
        Car_wrong = Car_wrong.tolist()
        Car_missing = Car_missing.tolist()
        persion_wrong = persion_wrong.tolist()
        persion_missing = persion_missing.tolist()
    data = {'distance':distance,'Car_wrong':Car_wrong,'Car_missing':Car_missing,'persion_wrong':persion_wrong,'persion_missing':persion_missing}
    return data