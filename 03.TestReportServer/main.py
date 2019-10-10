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

def selectbyTimeLDWTTC(x):
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




Situation = 140
starttime =0
endtime = 100000000000

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
#print(np.array(df['Timestamp'].tolist()))
#print(np.array(df['Timestamp'].tolist())[:,1])
#print(type(np.array(df['Timestamp'].tolist())[1,1]))
df = df.assign(Timestart=np.array(df['Timestamp'].tolist())[:,0],Timeend=np.array(df['Timestamp'].tolist())[:,1])
df = df[(df['Timestart'] >=starttime )&(df['Timeend'] <=endtime )].assign(selectlaber='yes')


LDW = df.groupby(df['selectlaber']).apply(lambda x: sumLDWTTC(x["LDW"]))
TTC = df.groupby(df['selectlaber']).apply(lambda x: sumLDWTTC(x["TTC"]))
version = LDW.index
LDW = (pd.DataFrame.to_numpy(LDW)).tolist()
TTC = (pd.DataFrame.to_numpy(TTC)).tolist()
version = (pd.DataFrame.to_numpy(version)).tolist()

Data = []
for i in range(len(version)):
    Data.append([version[i], LDW[i], TTC[i]])
# print(Data)
timesend = time.time()
print(timesend - timestart)
