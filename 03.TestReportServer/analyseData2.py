import pandas as pd
import numpy as np
import re
import os
import time
import matplotlib.pyplot as plt
import pymongo


def analyseData(DataFolder,filename):
    h = re.split('.bin', filename)
    orangeData_0x700 = pd.read_csv(os.path.join(DataFolder, h[0] + '_' + "0x700" + '_testresult.csv'))
    orangeData_0x780 = pd.read_csv(os.path.join(DataFolder, h[0] + '_' + "0x780" + '_testresult.csv'))
    orangeData_CarSpeed = pd.read_csv(os.path.join(DataFolder, h[0] + '_' + "0xa0" + '_testresult.csv'))

    print(orangeData_0x780.dtypes)
    Data = pd.merge(orangeData_0x700[['timestamp','Left LDW','Right LDW','fcw_on']],
                    orangeData_0x780[['timestamp', 'Left LDW', 'Right LDW', 'FCW Level']],
                    on='timestamp',how='outer')
    Data = Data.rename({'Left LDW_x': 'Left LDW_Mobileye',  'Right LDW_x':'Right LDW_Mobileye', 'fcw_on': 'TTC_Mobileye', 'Left LDW_y':'Left LDW_Jimu',
       'Right LDW_y':'Right LDW_Jimu', 'FCW Level':'TTC_Jimu'}, axis='columns')
    DataBackup = Data

    Data = Data[(Data['Left LDW_Mobileye']>0) | (Data['Right LDW_Mobileye']>0) |(Data['Left LDW_Jimu']>0 )|(Data['Right LDW_Jimu']>0) ].groupby((Data['timestamp']//3000)).agg({'timestamp':np.min, 'Left LDW_Mobileye':np.sum,'Right LDW_Mobileye':np.sum,'Left LDW_Jimu':np.sum,'Right LDW_Jimu':np.sum})
    Data = (pd.merge(Data.assign(ms10=Data['timestamp']//10),orangeData_CarSpeed.assign(ms10=orangeData_CarSpeed['timestamp']//10)[['ms10','speed']],on='ms10',how='left')).drop('ms10',axis=1)
    Data = (Data.groupby((Data['timestamp']-1500)//3000).agg({'timestamp':np.min, 'Left LDW_Mobileye':np.sum,'Right LDW_Mobileye':np.sum,'Left LDW_Jimu':np.sum,'Right LDW_Jimu':np.sum,'speed':np.min}))
    Data.insert(0,'时间',pd.to_datetime(Data['timestamp'].to_numpy()//1000,unit='s',utc=True).tz_convert('Asia/Shanghai'))
    LDW = np.array([[Data['Left LDW_Mobileye'][Data['Left LDW_Mobileye']>0].count(),0,0],
            [(Data['Left LDW_Jimu'][(Data['Left LDW_Jimu']>0)&(Data['Left LDW_Mobileye']>0) ]).count(),(Data['Left LDW_Jimu'][(Data['Left LDW_Jimu']<=0)&(Data['Left LDW_Mobileye']>0) ]).count(),Data['Left LDW_Jimu'][(Data['Left LDW_Jimu']>0)&(Data['Left LDW_Mobileye']<=0) ].count()],
            [Data['Right LDW_Mobileye'][Data['Right LDW_Mobileye']>0].count(),0,0],
            [Data['Right LDW_Jimu'][(Data['Right LDW_Jimu'] > 0) & (Data['Right LDW_Mobileye'] > 0)].count(),Data['Right LDW_Jimu'][(Data['Right LDW_Jimu'] <= 0) & (Data['Right LDW_Mobileye'] > 0)].count(),Data['Right LDW_Jimu'][(Data['Right LDW_Jimu'] > 0) & (Data['Right LDW_Mobileye'] <= 0)].count()]])
    LDW =pd.DataFrame(np.row_stack((LDW,np.row_stack((LDW[0,:]+LDW[ 2,:],LDW[1,:]+LDW[ 3,:],)))),index=['Mobileye LDW左','Jimu LDW左','Mobileye LDW右','Jimu LDW右','Mobileye Total','Jimu Total'],columns=['Right','Missing','Wrong'])
    LDW = LDW.assign(Right_ratio=LDW['Right']/([(LDW['Right'].to_numpy())[k//2*2] for k in range(len(LDW['Right'].to_numpy()))]),Missing_ratio=LDW['Missing']/([(LDW['Right'].to_numpy())[k//2*2] for k in range(len(LDW['Right'].to_numpy()))]),Wrong_ratio=LDW['Wrong']/([(LDW['Right'].to_numpy())[k//2*2] for k in range(len(LDW['Right'].to_numpy()))]))
    LDW_specific = Data

    Data =   DataBackup
    print(Data.dtypes)
    Data = Data[(Data['TTC_Mobileye']>0) | (Data['TTC_Jimu']>0)].groupby((Data['timestamp']//3000)).agg({'timestamp':np.min, 'TTC_Mobileye':np.sum,'TTC_Jimu':np.sum,})
    Data = (pd.merge(Data.assign(ms10=Data['timestamp']//10),orangeData_CarSpeed.assign(ms10=orangeData_CarSpeed['timestamp']//10)[['ms10','speed']],on='ms10',how='left')).drop('ms10',axis=1)
    Data = (Data.groupby((Data['timestamp']-1500)//3000).agg({'timestamp':np.min, 'TTC_Mobileye':np.sum,'TTC_Jimu':np.sum,'speed':np.min}))
    Data.insert(0,'时间',pd.to_datetime(Data['timestamp'].to_numpy()//1000,unit='s',utc=True).tz_convert('Asia/Shanghai'))
    TTC = np.array([[Data['TTC_Mobileye'][Data['TTC_Mobileye']>0].count(),0,0],
            [(Data['TTC_Jimu'][(Data['TTC_Mobileye']>0)&(Data['TTC_Jimu']>0) ]).count(),(Data['TTC_Jimu'][(Data['TTC_Jimu']<=0)&(Data['TTC_Mobileye']>0) ]).count(),Data['TTC_Jimu'][(Data['TTC_Jimu']>0)&(Data['TTC_Mobileye']<=0) ].count()]])
    TTC =pd.DataFrame(TTC,index=['TTC_Mobileye','TTC_Jimu'],columns=['Right','Missing','Wrong'])
    TTC = TTC.assign(Right_ratio=TTC['Right']/([(TTC['Right'].to_numpy())[k//2*2] for k in range(len(TTC['Right'].to_numpy()))]),Missing_ratio=TTC['Missing']/([(TTC['Right'].to_numpy())[k//2*2] for k in range(len(TTC['Right'].to_numpy()))]),Wrong_ratio=TTC['Wrong']/([(TTC['Right'].to_numpy())[k//2*2] for k in range(len(TTC['Right'].to_numpy()))]))
    TTC_specific = Data

    saveMongoDBdict = {'OrangeBinData':filename,
                       "Time":orangeData_0x780.iloc[0, 0] + '~' +orangeData_0x780.iloc[len(orangeData_0x780) - 1, 0],
                       'Timestamp': [orangeData_0x780.iloc[0, 1].tolist(),orangeData_0x780.iloc[len(orangeData_0x780) - 1, 1].tolist()],
                       'LDW':(LDW.iloc[:,:3].to_numpy()).tolist(),
                       'TTC':(TTC.iloc[:,:3].to_numpy()).tolist(),
                       'LDW_specific': (LDW_specific.iloc[:, :].to_numpy()).tolist(),
                       'TTC_specific': (TTC_specific.iloc[:, :].to_numpy()).tolist(),
                        }
    print(saveMongoDBdict)
    myclient = pymongo.MongoClient('mongodb://47.111.16.22:27017/')
    mydb = myclient["jimu_TestResult"]
    mycol = mydb["LDW"]
    #mycol.insert_one(saveMongoDBdict)
    myquery = {"OrangeBinData": filename}
    newvalues = {"$set": saveMongoDBdict}
    mycol.update_one(myquery,newvalues,True)

    












