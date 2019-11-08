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
    ##print(Summarylist)
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
    ##print(Summarylist)
    if len(Summarylist)==0:
        return {}
    else:
        return {"Data":Summarylist}


def deleteoneitem(filename):
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]
    myquery = {"OrangeBinData": {"$regex":str(filename)}}
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
    if 'LDW' in data:
        LDW = (np.array(data['LDW'])).astype(np.float)
        T = [LDW[:, 0] / ([LDW[:, 0][k // 2 * 2] for k in range(len(LDW[:, 0]))]),
             LDW[:, 1] / ([LDW[:, 0][k // 2 * 2] for k in range(len(LDW[:, 0]))]),
             LDW[:, 2] / ([LDW[:, 0][k // 2 * 2] for k in range(len(LDW[:, 0]))])]
        for i in range(len(T)):
            LDW = np.insert(LDW, len(LDW[0, :]), values=T[i], axis=1)
        TTC = (np.array(data['TTC'])).astype(np.float)
        T = [TTC[:, 0] / ([TTC[:, 0][k // 2 * 2] for k in range(len(TTC[:, 0]))]),
             TTC[:, 1] / ([TTC[:, 0][k // 2 * 2] for k in range(len(TTC[:, 0]))]),
             TTC[:, 2] / ([TTC[:, 0][k // 2 * 2] for k in range(len(TTC[:, 0]))])]
        for i in range(len(T)):
            TTC = np.insert(TTC, len(TTC[0, :]), values=T[i], axis=1)
        LDW[np.isinf(LDW)] = 0
        TTC[np.isinf(TTC)] = 0
        LDW = np.nan_to_num(LDW)
        TTC = np.nan_to_num(TTC)
        data['LDW'] = LDW.tolist()
        data['TTC'] = TTC.tolist()
    if 'TTC_manul' in data:
        TTC_manul = (np.array(data['TTC_manul'])).astype(np.float)
        T = [TTC_manul[:, 0] / ([TTC_manul[:, 0][k // 2 * 2] for k in range(len(TTC_manul[:, 0]))]),
             TTC_manul[:, 1] / ([TTC_manul[:, 0][k // 2 * 2] for k in range(len(TTC_manul[:, 0]))]),
             TTC_manul[:, 2] / ([TTC_manul[:, 0][k // 2 * 2] for k in range(len(TTC_manul[:, 0]))])]
        for i in range(len(T)):
            TTC_manul = np.insert(TTC_manul, len(TTC_manul[0, :]), values=T[i], axis=1)
        TTC_manul[np.isinf(TTC_manul)] = 0
        TTC_manul = np.nan_to_num(TTC_manul)
        data['TTC_manul'] = TTC_manul.tolist()

    ##print(data)
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

    df = pd.DataFrame(list(mycol.find({"LDW": {'$exists':True}})))
    df['Situation'] = pd.Series(list(map(jointliststr, (df['Situation']).tolist())))

    if Situation != 140:
        pd_Situation = pd.DataFrame({"Situation": Situation})
        pd_Situation["BigClass"] = pd_Situation["Situation"].apply(splitstr)
        conditions = list(pd_Situation.groupby(pd_Situation['BigClass']).apply(lambda x: sumstr(x["Situation"])))
        for i in range(len(conditions)):
            df = df[df['Situation'].str.contains(conditions[i])]
    # ##print(df)

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



def getDataByTime_TTC_manul(starttime,endtime,Situation):
    timestart = time.time()
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_row', None)
    np.set_printoptions(threshold=100000)
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]

    df = pd.DataFrame(list(mycol.find({"TTC_manul": {'$exists':True}})))

    df['Situation'] = pd.Series(list(map(jointliststr, (df['Situation']).tolist())))

    if Situation != 140:
        pd_Situation = pd.DataFrame({"Situation": Situation})
        pd_Situation["BigClass"] = pd_Situation["Situation"].apply(splitstr)
        conditions = list(pd_Situation.groupby(pd_Situation['BigClass']).apply(lambda x: sumstr(x["Situation"])))
        for i in range(len(conditions)):
            df = df[df['Situation'].str.contains(conditions[i])]
    # ##print(df)

    df = df.assign(Timestart=np.array(df['Timestamp'].tolist())[:, 0], Timeend=np.array(df['Timestamp'].tolist())[:, 1])
    df = df[(df['Timestart'] >= starttime) & (df['Timeend'] <= endtime)].assign(selectlaber='yes')


   # LDW = df.groupby(df['selectlaber']).apply(lambda x: sumLDWTTC(x["LDW"]))
    TTC_manul = df.groupby(df['selectlaber']).apply(lambda x: sumLDWTTC(x["TTC_manul"]))

    ##print(TTC_manul)

    #LDW = LDW.tolist()[0]
    TTC_manul = TTC_manul.tolist()[0]

    data={}
    data['LDW'] = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    data['TTC_manul'] = TTC_manul

    TTC_manul = pd.DataFrame(TTC_manul,
                       index=['TTC_manual','TTC_Jimu'], columns=['Right', 'Missing', 'Wrong','Right_ratio','Missing_ratio','Wrong_ratio'])

    TTC_manul.iloc[:, :3].plot.bar(stacked=True, figsize=(8, 8),
                             title='TTC告警对比分析：与手工标注的正确结果进行对比\n'  )
    [(plt.text(k * 2 + 1, (TTC_manul.iloc[1::2, :3].to_numpy())[k, 0], '%d' % (TTC_manul.iloc[1::2, :3].to_numpy())[k, 0],
               ha='center', va='top'),
      plt.text(k * 2 + 1, (TTC_manul.iloc[1::2, :3].to_numpy())[k, :2].sum(), '%d' % (TTC_manul.iloc[1::2, :3].to_numpy())[k, 1],
               ha='center', va='top'),
      plt.text(k * 2 + 1, (TTC_manul.iloc[1::2, :3].to_numpy())[k, :3].sum(), '%d' % (TTC_manul.iloc[1::2, :3].to_numpy())[k, 2],
               ha='center', va='top')) for k in range(len(TTC_manul.iloc[1::2, 2].to_numpy()))]
    [(plt.text(k * 2, (TTC_manul.iloc[0::2, :3].to_numpy())[k, 0], '%d' % (TTC_manul.iloc[0::2, :3].to_numpy())[k, 0], ha='center',
               va='top')) for k in range(len(TTC_manul.iloc[0::2, 2].to_numpy()))]
    plt.xticks(rotation=30)
    plt.savefig('TTC_manul.png')
    plt.close()
    image = imageToStr('TTC_manul.png')
    data['TTC_manul_bar'] = image

    return data





def getdatabyversionAll(Situation,starttime,endtime):
    timestart = time.time()
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_row', None)
    np.set_printoptions(threshold=100000)
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]

    df = pd.DataFrame(list(mycol.find({"LDW": {'$exists':True}})))
    if len(df)==0:
        return {}
    df['Situation'] = pd.Series(list(map(jointliststr, (df['Situation']).tolist())))

    if Situation != 140:
        pd_Situation = pd.DataFrame({"Situation": Situation})
        pd_Situation["BigClass"] = pd_Situation["Situation"].apply(splitstr)
        conditions = list(pd_Situation.groupby(pd_Situation['BigClass']).apply(lambda x: sumstr(x["Situation"])))
        for i in range(len(conditions)):
            df = df[df['Situation'].str.contains(conditions[i])]
    ###print(df)
    if len(df)==0:
        return {}
    if float(starttime) > 0 and float(starttime) < float(endtime):
        ##print(df)
        df = df.assign(Timestart=np.array(df['Timestamp'].tolist())[:, 0],
                       Timeend=np.array(df['Timestamp'].tolist())[:, 1])
        df = df[(df['Timestart'] >= float(starttime)) & (df['Timeend'] <= float(endtime))]
    if len(df)==0:
        return {}

    LDW = df.groupby(df['version']).apply(lambda x:sumLDWTTC(x["LDW"]))
    TTC = df.groupby(df['version']).apply(lambda x:sumLDWTTC(x["TTC"]))

    df['version'] = '总计'
    LDW_ALL = df.groupby(df['version']).apply(lambda x: sumLDWTTC(x["LDW"]))
    TTC_ALL = df.groupby(df['version']).apply(lambda x: sumLDWTTC(x["TTC"]))
    LDW = pd.concat([LDW,LDW_ALL])
    TTC = pd.concat(([TTC,TTC_ALL]))

    version = LDW.index
    LDW = (pd.DataFrame.to_numpy( LDW)).tolist()
    TTC = (pd.DataFrame.to_numpy( TTC)).tolist()
    version = (pd.DataFrame.to_numpy(version)).tolist()

    Data = []
    for i in range(len(version)):
        Data.append([version[i],LDW[i],TTC[i]])
    ###print(Data)
    timesend = time.time()
    ##print(timesend - timestart)
    return {'data': Data}



def getdatabyversionAll_TTC_manual(Situation,starttime,endtime):
    timestart = time.time()
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_row', None)
    np.set_printoptions(threshold=100000)
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]

    df = pd.DataFrame(list(mycol.find({"TTC_manul": {'$exists':True}})))

    if len(df)==0:
        return {}

    df['Situation'] = pd.Series(list(map(jointliststr, (df['Situation']).tolist())))

    if Situation != 140:
        pd_Situation = pd.DataFrame({"Situation": Situation})
        pd_Situation["BigClass"] = pd_Situation["Situation"].apply(splitstr)
        conditions = list(pd_Situation.groupby(pd_Situation['BigClass']).apply(lambda x: sumstr(x["Situation"])))
        for i in range(len(conditions)):
            df = df[df['Situation'].str.contains(conditions[i])]
    if len(df) == 0:
        return {}
    if float(starttime)>0 and float(starttime)<float(endtime):
        df = df.assign(Timestart=np.array(df['Timestamp'].tolist())[:, 0],
                       Timeend=np.array(df['Timestamp'].tolist())[:, 1])
        df = df[(df['Timestart'] >= float(starttime)) & (df['Timeend'] <= float(endtime))]
    if len(df)==0:
        return {}

    #LDW = df.groupby(df['version']).apply(lambda x:sumLDWTTC(x["LDW"]))
    TTC_manul = df.groupby(df['version']).apply(lambda x:sumLDWTTC(x["TTC_manul"]))

    df['version'] = '总计'
    TTC_manul_ALL = df.groupby(df['version']).apply(lambda x: sumLDWTTC(x["TTC_manul"]))
    TTC_manul = pd.concat([TTC_manul,TTC_manul_ALL])
    version = TTC_manul.index
    #LDW = (pd.DataFrame.to_numpy( LDW)).tolist()
    TTC_manul = (pd.DataFrame.to_numpy( TTC_manul)).tolist()
    version = (pd.DataFrame.to_numpy(version)).tolist()

    Data = []
    LDW=[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    for i in range(len(version)):
        Data.append([version[i],LDW,TTC_manul[i]])
    ###print(Data)
    timesend = time.time()
    ##print(timesend - timestart)
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
    if len(df)==0:
        return {}
    df['Situation'] = pd.Series(list(map(jointliststr, (df['Situation']).tolist())))

    if Situation != 140:
        pd_Situation = pd.DataFrame({"Situation": Situation})
        pd_Situation["BigClass"] = pd_Situation["Situation"].apply(splitstr)
        conditions = list(pd_Situation.groupby(pd_Situation['BigClass']).apply(lambda x: sumstr(x["Situation"])))
        for i in range(len(conditions)):
            df = df[df['Situation'].str.contains(conditions[i])]
    # ##print(df)

    df = df.assign(Timestart=np.array(df['Timestamp'].tolist())[:, 0], Timeend=np.array(df['Timestamp'].tolist())[:, 1])
    df = df[(df['Timestart'] >= starttime) & (df['Timeend'] <= endtime)].assign(selectlaber='yes')

    df[['distance', 'Car_wrong', 'Car_missing', 'persion_wrong', 'persion_missing']] = df[
        ['distance', 'Car_wrong', 'Car_missing', 'persion_wrong', 'persion_missing']].astype(float)
    df = df.groupby(df['selectlaber']).agg(
        { 'distance': np.sum, 'Car_wrong': np.sum, 'Car_missing': np.sum, 'persion_wrong': np.sum,
         'persion_missing': np.sum})

    Data = pd.DataFrame.to_numpy( df)[0]

    timesend = time.time()
    ##print(timesend - timestart)

    data = {'distance':Data[0],'Car_wrong':Data[1],'Car_missing':Data[2],'persion_wrong':Data[3],'persion_missing':Data[4]}
    return data




def getdatabyversionmissingwrongAll(Situation,starttime,endtime):
    timestart = time.time()
    pd.set_option('expand_frame_repr', False)
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["MissingWrong"]

    df = pd.DataFrame(list(mycol.find({"Car_wrong": {'$exists':True}})))
    if len(df)==0:
        return {}
    df['Situation'] = pd.Series(list(map(jointliststr, (df['Situation']).tolist())))

    if Situation != 140:
        pd_Situation = pd.DataFrame({"Situation": Situation})
        pd_Situation["BigClass"] = pd_Situation["Situation"].apply(splitstr)
        conditions = list(pd_Situation.groupby(pd_Situation['BigClass']).apply(lambda x: sumstr(x["Situation"])))
        #print(conditions)
        for i in range(len(conditions)):
            df = df[ df['Situation'].str.contains(conditions[i])]

    if len(df)==0:
        return {}

    if float(starttime) > 0 and float(starttime) < float(endtime):
        df = df.assign(Timestart=np.array(df['Timestamp'].tolist())[:, 0],
                       Timeend=np.array(df['Timestamp'].tolist())[:, 1])
        df = df[(df['Timestart'] >= float(starttime)) & (df['Timeend'] <= float(endtime))]
    if len(df)==0:
        return {}

    ##print(df)
    df_base = df[['version','distance']]
    df_base[['distance']] = df_base[['distance']].astype(float)
    df_base =  df_base.groupby(df_base['version']).agg({'version': np.min, 'distance': np.sum})
    df_base.index.name = None


    statlist=['Car_wrong', 'Car_missing', 'persion_wrong', 'persion_missing','mobileyeCar_wrong', 'mobileyeCar_missing', 'mobileyepersion_wrong', 'mobileyepersion_missing']
    #statlist=['Car_wrong']

    for item in statlist:
        NONE_VIN = (df[item].isnull()) | (df[item].apply(lambda x: (x=='')))
        #df_null = df[NONE_VIN]
        df_select = df[~NONE_VIN]
        df_singleData = df_select[['version', 'distance',item]]
        df_singleData[['distance',item]] = df_singleData[['distance',item]].astype(float)
        df_singleData = df_singleData.groupby(df_singleData['version']).agg({'version': np.min, 'distance': np.sum,item:np.sum})
        df_singleData.index.name = None
        df_singleData = df_singleData.rename({'distance': 'distance' + item}, axis='columns')
        ###print(df_singleData)
        df_base = (pd.merge(df_base, df_singleData, on='version',how='left'))
    df_all = df_base.sum()
    df_all['version'] = '总计'
    df_all = pd.DataFrame(df_all.to_numpy().reshape(1,len(df_all)),columns=df_base.columns)
    df_base = pd.concat([df_base,df_all])

    df_base.fillna(-1, inplace=True)

    timesend = time.time()

    Data = df_base.to_numpy().tolist()
    return {'data': Data}


def uploadTTC(json_data):
    ID = json_data['ID']
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]

    appdex=['.bin','.dat']
    ID_full=[]
    for item in appdex:
        data = mycol.find_one({"OrangeBinData":ID+item })
        if data:
            ID_full=ID+item
            break
    if not ID_full:
        return {}
    timestamp_TTC = json_data['timestamp_TTC']
    TTC_manul = pd.DataFrame({"timestamp":timestamp_TTC,'TTC':1})
    if 'jimu_TTC_specific' in data:
        TTC_ADAS = pd.DataFrame(data['jimu_TTC_specific'],columns=['Date','timestamp','TTC_Jimu'])
    else:
        TTC_ADAS = pd.DataFrame(data['TTC_specific'],columns=['Date', 'timestamp', 'TTC_Mobileye', 'TTC_Jimu', 'speed'])
    ##print(TTC_manul)

    if  len(TTC_manul)==0 and len(TTC_ADAS)==0:
        myquery = {"OrangeBinData": ID_full}
        mycol.update_one(myquery, {'$set': {"TTC_manul":[[0,0,0],[0,0,0]], "TTC_manul_specific": []}}, upsert=False)
        return


    Data = pd.merge(TTC_manul[['timestamp','TTC']],
                    TTC_ADAS[['timestamp', 'TTC_Jimu']],
                    on='timestamp',how='outer')

    Data = Data[(Data['TTC']>0) | (Data['TTC_Jimu']>0)].groupby((Data['timestamp']//3000)).agg({'timestamp':np.min, 'TTC':np.sum,'TTC_Jimu':np.sum})
    Data.insert(0, '时间',pd.to_datetime(Data['timestamp'].to_numpy() // 1000, unit='s', utc=True).tz_convert('Asia/Shanghai'))

    TTC = np.array([[Data['TTC'][Data['TTC'] > 0].count(), 0, 0],
                    [(Data['TTC_Jimu'][(Data['TTC'] > 0) & (Data['TTC_Jimu'] > 0)]).count(),
                     (Data['TTC_Jimu'][(Data['TTC_Jimu'] <= 0) & (Data['TTC'] > 0)]).count(),
                     Data['TTC_Jimu'][(Data['TTC_Jimu'] > 0) & (Data['TTC'] <= 0)].count()]])
    TTC = pd.DataFrame(TTC, index=['TTC', 'TTC_Jimu'], columns=['Right', 'Missing', 'Wrong'])
    TTC = TTC.assign(Right_ratio=TTC['Right'] / (
    [(TTC['Right'].to_numpy())[k // 2 * 2] for k in range(len(TTC['Right'].to_numpy()))]),
                     Missing_ratio=TTC['Missing'] / (
                     [(TTC['Right'].to_numpy())[k // 2 * 2] for k in range(len(TTC['Right'].to_numpy()))]),
                     Wrong_ratio=TTC['Wrong'] / (
                     [(TTC['Right'].to_numpy())[k // 2 * 2] for k in range(len(TTC['Right'].to_numpy()))]))
    Data.fillna(0, inplace=True)
    TTC_manul = TTC
    TTC_manul_specific = Data
    myquery = {"OrangeBinData": ID_full}
    #newvalues = {"$set": saveMongoDBdict}
    mycol.update_one(myquery, {'$set': {"TTC_manul":TTC_manul.iloc[:,:3].to_numpy().tolist(),"TTC_manul_specific":TTC_manul_specific.to_numpy().tolist()}}, upsert=False)


def delectTTC_manul(json_data):
    ID = json_data['ID']
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]

    data = mycol.find_one({"OrangeBinData":{"$regex":ID}})#{post_text: {$regex: "runoob"}}
    mycol.update_one({"OrangeBinData":{"$regex":ID}}, {'$unset': {"TTC_manul": 1,"TTC_manul_specific":1}})

