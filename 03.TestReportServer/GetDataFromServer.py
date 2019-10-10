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

def jointliststr(c):
    return ' '.join(c)

def sumstr(x):
    return '|'.join(x)

def splitstr(x):
    t = x.split("-")
    return t[0]

def sumLDWTTC(x):
    x = list(x)
    if len(x)<1:
        return []
    LDWTTC = np.array(x[0]).astype(np.float)
    for i in range(1,len(x)):
        LDWTTC = LDWTTC + np.array(x[i]).astype(np.float)
    T = [LDWTTC[:,0]/([LDWTTC[:,0][k//2*2] for k in range(len(LDWTTC[:,0]))]),LDWTTC[:,1]/([LDWTTC[:,0][k//2*2] for k in range(len(LDWTTC[:,0]))]),LDWTTC[:,2]/([LDWTTC[:,0][k//2*2] for k in range(len(LDWTTC[:,0]))])]
    for i in range(len(T)):
        LDWTTC = np.insert(LDWTTC,len(LDWTTC[0,:]), values=T[i], axis=1)
    LDWTTC[np.isinf(LDWTTC)] = 0
    LDWTTC = np.nan_to_num(LDWTTC)
    return LDWTTC.tolist()


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


def deleteoneitem(filename):
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]
    myquery = {"OrangeBinData": filename}
    mycol.delete_one(myquery)
    return {}


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
    data.pop("_id")
    LDW = (np.array(data['LDW'])).astype(np.float)
    T = [LDW[:,0]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))]),LDW[:,1]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))]),LDW[:,2]/([LDW[:,0][k//2*2] for k in range(len(LDW[:,0]))])]
    for i in range(len(T)):
        LDW = np.insert(LDW,len(LDW[0,:]), values=T[i], axis=1)
    TTC = (np.array(data['TTC'])).astype(np.float)
    T = [TTC[:,0]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))]),TTC[:,1]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))]),TTC[:,2]/([TTC[:,0][k//2*2] for k in range(len(TTC[:,0]))])]
    for i in range(len(T)):
        TTC = np.insert(TTC,len(TTC[0,:]), values=T[i], axis=1)
    LDW[np.isinf(LDW)] = 0
    TTC[np.isinf(TTC)] = 0
    LDW = np.nan_to_num(LDW)
    TTC = np.nan_to_num(TTC)
    data['LDW'] = LDW.tolist()
    data['TTC'] = TTC.tolist()
    print(data)

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
    timestart = time.time()
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_row', None)
    np.set_printoptions(threshold=100000)
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]

    df = pd.DataFrame(list(mycol.find()))
    df['Situation'] = pd.Series(list(map(jointliststr, (df['Situation']).tolist())))

    if Situation != 140:
        pd_Situation = pd.DataFrame({"Situation": Situation})
        pd_Situation["BigClass"] = pd_Situation["Situation"].apply(splitstr)
        conditions = list(pd_Situation.groupby(pd_Situation['BigClass']).apply(lambda x: sumstr(x["Situation"])))
        for i in range(len(conditions)):
            df = df[df['Situation'].str.contains(conditions[i])]
    # print(df)

    df = df.assign(Timestart=np.array(df['Timestamp'].tolist())[:, 0], Timeend=np.array(df['Timestamp'].tolist())[:, 1])
    df = df[(df['Timestart'] >= starttime) & (df['Timeend'] <= endtime)].assign(selectlaber='yes')
    LDW = df.groupby(df['selectlaber']).apply(lambda x: sumLDWTTC(x["LDW"]))
    TTC = df.groupby(df['selectlaber']).apply(lambda x: sumLDWTTC(x["TTC"]))

    LDW = LDW.tolist()[0]
    TTC = TTC.tolist()[0]

    data={}
    data['LDW'] = LDW
    data['TTC'] = TTC

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

    return data



def getdatabyversionAll(Situation):
    timestart = time.time()
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_row', None)
    np.set_printoptions(threshold=100000)
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]

    df = pd.DataFrame(list(mycol.find()))
    df['Situation'] = pd.Series(list(map(jointliststr, (df['Situation']).tolist())))

    if Situation != 140:
        pd_Situation = pd.DataFrame({"Situation": Situation})
        pd_Situation["BigClass"] = pd_Situation["Situation"].apply(splitstr)
        conditions = list(pd_Situation.groupby(pd_Situation['BigClass']).apply(lambda x: sumstr(x["Situation"])))
        for i in range(len(conditions)):
            df = df[df['Situation'].str.contains(conditions[i])]
    #print(df)


    LDW = df.groupby(df['version']).apply(lambda x:sumLDWTTC(x["LDW"]))
    TTC = df.groupby(df['version']).apply(lambda x:sumLDWTTC(x["TTC"]))
    version = LDW.index
    LDW = (pd.DataFrame.to_numpy( LDW)).tolist()
    TTC = (pd.DataFrame.to_numpy( TTC)).tolist()
    version = (pd.DataFrame.to_numpy(version)).tolist()

    Data = []
    for i in range(len(version)):
        Data.append([version[i],LDW[i],TTC[i]])
    #print(Data)
    timesend = time.time()
    print(timesend - timestart)
    return {'data': Data}





#

def getDataByTimemissingwrong(starttime,endtime,Situation):
    timestart = time.time()
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_row', None)
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["MissingWrong"]

    df = pd.DataFrame(list(mycol.find()))
    df['Situation'] = pd.Series(list(map(jointliststr, (df['Situation']).tolist())))

    if Situation != 140:
        pd_Situation = pd.DataFrame({"Situation": Situation})
        pd_Situation["BigClass"] = pd_Situation["Situation"].apply(splitstr)
        conditions = list(pd_Situation.groupby(pd_Situation['BigClass']).apply(lambda x: sumstr(x["Situation"])))
        for i in range(len(conditions)):
            df = df[df['Situation'].str.contains(conditions[i])]
    # print(df)

    df = df.assign(Timestart=np.array(df['Timestamp'].tolist())[:, 0], Timeend=np.array(df['Timestamp'].tolist())[:, 1])
    df = df[(df['Timestart'] >= starttime) & (df['Timeend'] <= endtime)].assign(selectlaber='yes')

    df[['distance', 'Car_wrong', 'Car_missing', 'persion_wrong', 'persion_missing']] = df[
        ['distance', 'Car_wrong', 'Car_missing', 'persion_wrong', 'persion_missing']].astype(float)
    df = df.groupby(df['selectlaber']).agg(
        { 'distance': np.sum, 'Car_wrong': np.sum, 'Car_missing': np.sum, 'persion_wrong': np.sum,
         'persion_missing': np.sum})

    Data = pd.DataFrame.to_numpy( df)[0]

    timesend = time.time()
    print(timesend - timestart)

    data = {'distance':Data[0],'Car_wrong':Data[1],'Car_missing':Data[2],'persion_wrong':Data[3],'persion_missing':Data[4]}
    return data




def getdatabyversionmissingwrongAll(Situation):
    timestart = time.time()
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_row', None)
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["MissingWrong"]

    df = pd.DataFrame(list(mycol.find()))
    df['Situation'] = pd.Series(list(map(jointliststr, (df['Situation']).tolist())))

    if Situation != 140:
        pd_Situation = pd.DataFrame({"Situation": Situation})
        pd_Situation["BigClass"] = pd_Situation["Situation"].apply(splitstr)
        conditions = list(pd_Situation.groupby(pd_Situation['BigClass']).apply(lambda x: sumstr(x["Situation"])))
        for i in range(len(conditions)):
            df = df[ df['Situation'].str.contains(conditions[i])]
    #print(df)

    df[['distance', 'Car_wrong', 'Car_missing', 'persion_wrong', 'persion_missing']] = df[['distance', 'Car_wrong', 'Car_missing', 'persion_wrong', 'persion_missing']].astype(float)
    df = df.groupby(df['version']).agg( {'version': np.min, 'distance': np.sum, 'Car_wrong': np.sum, 'Car_missing': np.sum, 'persion_wrong': np.sum,  'persion_missing': np.sum})
    Data = (np.array(df)).tolist()
    print(Data)
    timesend = time.time()

    print(timesend - timestart)
    return {'data': Data}


