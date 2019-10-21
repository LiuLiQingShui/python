import pandas as pd
import numpy as np
import re
import os
import time
import matplotlib.pyplot as plt
import math


def analyseData(DataFolder,filename):
    print(DataFolder,filename)
    h=re.split('.bin|.dat', filename)

    orangeData_0x780 = pd.read_csv(os.path.join(DataFolder, h[0] + '_' + "0x780" + '_testresult.csv'))

    Data_jimu_LDW = orangeData_0x780[['timestamp', 'Left LDW', 'Right LDW']]
    Data_jimu_LDW = Data_jimu_LDW[(Data_jimu_LDW['Left LDW']>0) | (Data_jimu_LDW['Right LDW']>0)].groupby((Data_jimu_LDW['timestamp']//3000)).agg({'timestamp':np.min, 'Left LDW':np.sum,'Right LDW':np.sum})
    Data_jimu_LDW.insert(0, '时间',pd.to_datetime(Data_jimu_LDW['timestamp'].to_numpy() // 1000, unit='s', utc=True).tz_convert('Asia/Shanghai'))
    Data_jimu_LDW.to_csv(os.path.join(DataFolder, h[0] + '_Jimu_LDW_specific.csv'), encoding='utf_8_sig', index=False)

    Data_jimu_TTC = orangeData_0x780[['timestamp', 'FCW Level']]
    Data_jimu_TTC = Data_jimu_TTC.rename({ 'FCW Level':'TTC_Jimu'}, axis='columns')
    Data_jimu_TTC = Data_jimu_TTC[(Data_jimu_TTC['TTC_Jimu']>0)].groupby((Data_jimu_TTC['timestamp']//3000)).agg({'timestamp':np.min, 'TTC_Jimu':np.sum})
    Data_jimu_TTC.insert(0, '时间',pd.to_datetime(Data_jimu_TTC['timestamp'].to_numpy() // 1000, unit='s', utc=True).tz_convert('Asia/Shanghai'))
    Data_jimu_TTC.to_csv(os.path.join(DataFolder, h[0] + '_Jimu_TTC_specific.csv'), encoding='utf_8_sig', index=False)


    if os.path.exists(os.path.join(DataFolder, h[0] + '_' + "0xa0" + '_testresult.csv')):
        orangeData_CarSpeed = pd.read_csv(os.path.join(DataFolder, h[0] + '_' + "0xa0" + '_testresult.csv'))
        turn = pd.read_csv(os.path.join(DataFolder, h[0] + '_' + "0x23a" + '_testresult.csv'))
        turn = pd.DataFrame({'timestamp': turn['timestamp'],
                             'turn': (((turn['right'].to_numpy().astype(int)) << 1) | (
                                 turn['left'].to_numpy().astype(int)))
                             })
        orangeData_CarSpeed = (pd.merge(orangeData_CarSpeed.assign(ms10=orangeData_CarSpeed['timestamp'] // 10),turn.assign(ms10=turn['timestamp'] // 10)[['ms10','turn']],on='ms10', how='left')).drop('ms10', axis=1)
        orangeData_CarSpeed = orangeData_CarSpeed.fillna(method='pad')
    elif os.path.exists(os.path.join(DataFolder, h[0] + '_' + "0x68" + '_testresult.csv')):
        orangeData_CarSpeed = pd.read_csv(os.path.join(DataFolder, h[0] + '_' + "0x68" + '_testresult.csv'))
        orangeData_CarSpeed = pd.DataFrame({'timestamp':orangeData_CarSpeed['timestamp'],
                                            'speed': (((orangeData_CarSpeed['speed_h'].to_numpy().astype(int))<<5)|(orangeData_CarSpeed['speed_l'].to_numpy().astype(int)))* 0.05625 * 100,
                                            })
        turn = pd.read_csv(os.path.join(DataFolder, h[0] + '_' + "0x2d4" + '_testresult.csv'))
        turn = pd.DataFrame({'timestamp':turn['timestamp'],
                                            'turn': (((turn['right'].to_numpy().astype(int))<<1)|(turn['left'].to_numpy().astype(int)))
                                            })
        brake = pd.read_csv(os.path.join(DataFolder, h[0] + '_' + "0xe2" + '_testresult.csv'))
        brake = pd.DataFrame({'timestamp':brake['timestamp'],
                                            'brake': np.floor(brake['brake'].to_numpy().astype(int)/2)
                                            })
       # print(brake)
        orangeData_CarSpeed = (pd.merge(orangeData_CarSpeed.assign(ms10=orangeData_CarSpeed['timestamp'] // 20),turn.assign(ms10=turn['timestamp'] // 20)[['ms10','turn']],on='ms10', how='left')).drop('ms10', axis=1)
        #print(orangeData_CarSpeed)
        orangeData_CarSpeed = (pd.merge(orangeData_CarSpeed.assign(ms10=orangeData_CarSpeed['timestamp'] // 20),brake.assign(ms10=brake['timestamp'] // 20)[['ms10','brake']],on='ms10', how='left')).drop('ms10', axis=1)
        orangeData_CarSpeed = orangeData_CarSpeed.fillna(method='pad')
    else:
        print('Info: No car speed found. filled it with zero')
        orangeData_CarSpeed = orangeData_0x780['timestamp']
        orangeData_CarSpeed = pd.DataFrame({'timestamp':orangeData_CarSpeed,
                                            'speed':-1,
                                            'turn': -1,
                                            'brake': -1
        })
    orangeData_CarSpeed.to_csv(os.path.join(DataFolder, h[0] + '_CarInformation.csv'), encoding='utf_8_sig',index=False)

    orangeData_CarSpeed = orangeData_CarSpeed.assign(ms10=orangeData_CarSpeed['timestamp'] // 10)[['ms10', 'speed']]
    orangeData_CarSpeed = orangeData_CarSpeed.groupby(orangeData_CarSpeed['ms10']).agg({'ms10':np.min, 'speed':np.max})
    orangeData_CarSpeed.index.name = None


    if  not os.path.exists(os.path.join(DataFolder, h[0] + '_' + "0x700" + '_testresult.csv')):
        print('Error: No Mobileye Data')
        time.sleep(5)
        return
    orangeData_0x700 = pd.read_csv(os.path.join(DataFolder, h[0] + '_' + "0x700" + '_testresult.csv'))


    Data = pd.merge(orangeData_0x700[['timestamp','Left LDW','Right LDW','fcw_on']],
                    orangeData_0x780[['timestamp', 'Left LDW', 'Right LDW', 'FCW Level']],
                    on='timestamp',how='outer')
    Data = Data.rename({'Left LDW_x': 'Left LDW_Mobileye',  'Right LDW_x':'Right LDW_Mobileye', 'fcw_on': 'TTC_Mobileye', 'Left LDW_y':'Left LDW_Jimu',
       'Right LDW_y':'Right LDW_Jimu', 'FCW Level':'TTC_Jimu'}, axis='columns')
    DataBackup = Data

    Data = Data[(Data['Left LDW_Mobileye']>0) | (Data['Right LDW_Mobileye']>0) |(Data['Left LDW_Jimu']>0 )|(Data['Right LDW_Jimu']>0) ].groupby((Data['timestamp']//3000)).agg({'timestamp':np.min, 'Left LDW_Mobileye':np.sum,'Right LDW_Mobileye':np.sum,'Left LDW_Jimu':np.sum,'Right LDW_Jimu':np.sum})
    Data = (pd.merge(Data.assign(ms10=Data['timestamp']//10),orangeData_CarSpeed,on='ms10',how='left')).drop('ms10',axis=1)
    Data = (Data.groupby((Data['timestamp']-1500)//3000).agg({'timestamp':np.min, 'Left LDW_Mobileye':np.sum,'Right LDW_Mobileye':np.sum,'Left LDW_Jimu':np.sum,'Right LDW_Jimu':np.sum,'speed':np.min}))
    Data.insert(0,'时间',pd.to_datetime(Data['timestamp'].to_numpy()//1000,unit='s',utc=True).tz_convert('Asia/Shanghai'))
    LDW = np.array([[Data['Left LDW_Mobileye'][Data['Left LDW_Mobileye']>0].count(),0,0],
            [(Data['Left LDW_Jimu'][(Data['Left LDW_Jimu']>0)&(Data['Left LDW_Mobileye']>0) ]).count(),(Data['Left LDW_Jimu'][(Data['Left LDW_Jimu']<=0)&(Data['Left LDW_Mobileye']>0) ]).count(),Data['Left LDW_Jimu'][(Data['Left LDW_Jimu']>0)&(Data['Left LDW_Mobileye']<=0) ].count()],
            [Data['Right LDW_Mobileye'][Data['Right LDW_Mobileye']>0].count(),0,0],
            [Data['Right LDW_Jimu'][(Data['Right LDW_Jimu'] > 0) & (Data['Right LDW_Mobileye'] > 0)].count(),Data['Right LDW_Jimu'][(Data['Right LDW_Jimu'] <= 0) & (Data['Right LDW_Mobileye'] > 0)].count(),Data['Right LDW_Jimu'][(Data['Right LDW_Jimu'] > 0) & (Data['Right LDW_Mobileye'] <= 0)].count()]])
    LDW =pd.DataFrame(np.row_stack((LDW,np.row_stack((LDW[0,:]+LDW[ 2,:],LDW[1,:]+LDW[ 3,:],)))),index=['Mobileye LDW左','Jimu LDW左','Mobileye LDW右','Jimu LDW右','Mobileye Total','Jimu Total'],columns=['Right','Missing','Wrong'])
    LDW = LDW.assign(Right_ratio=LDW['Right']/([(LDW['Right'].to_numpy())[k//2*2] for k in range(len(LDW['Right'].to_numpy()))]),Missing_ratio=LDW['Missing']/([(LDW['Right'].to_numpy())[k//2*2] for k in range(len(LDW['Right'].to_numpy()))]),Wrong_ratio=LDW['Wrong']/([(LDW['Right'].to_numpy())[k//2*2] for k in range(len(LDW['Right'].to_numpy()))]))
    plt.close('all')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    LDW.iloc[:,:3].plot.bar(stacked=True,figsize=(8,8),title='LDW告警对比分析：Jimu、Mobileye\n'+orangeData_0x780.iloc[0,0]+'~'+orangeData_0x780.iloc[len(orangeData_0x780)-1,0])
    [(plt.text(k*2+1, (LDW.iloc[1::2,:3].to_numpy())[k,0], '%d' % (LDW.iloc[1::2,:3].to_numpy())[k,0], ha='center', va='top'),plt.text(k*2+1, (LDW.iloc[1::2,:3].to_numpy())[k,:2].sum(), '%d' % (LDW.iloc[1::2,:3].to_numpy())[k,1], ha='center', va='top'),plt.text(k*2+1, (LDW.iloc[1::2,:3].to_numpy())[k,:3].sum(), '%d' % (LDW.iloc[1::2,:3].to_numpy())[k,2], ha='center', va='top')) for k in range(len(LDW.iloc[1::2,2].to_numpy()))]
    [(plt.text(k*2, (LDW.iloc[0::2,:3].to_numpy())[k,0], '%d' % (LDW.iloc[0::2,:3].to_numpy())[k,0], ha='center', va='top')) for k in range(len(LDW.iloc[0::2,2].to_numpy()))]
    plt.xticks(rotation=30)
    plt.savefig(os.path.join(DataFolder, h[0] + '_LDW.png'))
    plt.close()
    Data.to_csv(os.path.join(DataFolder, h[0] + '_LDW_specific.csv'),encoding='utf_8_sig',index=False)
    LDW.to_csv(os.path.join(DataFolder, h[0] + '_LDW.csv'), encoding='utf_8_sig')

    Data  =   DataBackup
    Data = Data[(Data['TTC_Mobileye']>0) | (Data['TTC_Jimu']>0)].groupby((Data['timestamp']//3000)).agg({'timestamp':np.min, 'TTC_Mobileye':np.sum,'TTC_Jimu':np.sum,})
    Data = (pd.merge(Data.assign(ms10=Data['timestamp']//10),orangeData_CarSpeed,on='ms10',how='left')).drop('ms10',axis=1)
    Data = (Data.groupby((Data['timestamp']-1500)//3000).agg({'timestamp':np.min, 'TTC_Mobileye':np.sum,'TTC_Jimu':np.sum,'speed':np.min}))
    Data.insert(0,'时间',pd.to_datetime(Data['timestamp'].to_numpy()//1000,unit='s',utc=True).tz_convert('Asia/Shanghai'))
    TTC = np.array([[Data['TTC_Mobileye'][Data['TTC_Mobileye']>0].count(),0,0],
            [(Data['TTC_Jimu'][(Data['TTC_Mobileye']>0)&(Data['TTC_Jimu']>0) ]).count(),(Data['TTC_Jimu'][(Data['TTC_Jimu']<=0)&(Data['TTC_Mobileye']>0) ]).count(),Data['TTC_Jimu'][(Data['TTC_Jimu']>0)&(Data['TTC_Mobileye']<=0) ].count()]])
    TTC =pd.DataFrame(TTC,index=['TTC_Mobileye','TTC_Jimu'],columns=['Right','Missing','Wrong'])
    TTC = TTC.assign(Right_ratio=TTC['Right']/([(TTC['Right'].to_numpy())[k//2*2] for k in range(len(TTC['Right'].to_numpy()))]),Missing_ratio=TTC['Missing']/([(TTC['Right'].to_numpy())[k//2*2] for k in range(len(TTC['Right'].to_numpy()))]),Wrong_ratio=TTC['Wrong']/([(TTC['Right'].to_numpy())[k//2*2] for k in range(len(TTC['Right'].to_numpy()))]))
    TTC.iloc[:, :3].plot.bar(stacked=True, figsize=(8, 8),title='TTC告警对比分析：Jimu、Mobileye\n' + orangeData_0x780.iloc[0, 0] + '~' +orangeData_0x780.iloc[len(orangeData_0x780) - 1, 0])
    [(plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, 0], '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 0], ha='center', va='top'),plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, :2].sum(), '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 1],ha='center', va='top'), plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, :3].sum(), '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 2], ha='center',va='top')) for k in range(len(TTC.iloc[1::2, 2].to_numpy()))]
    [(plt.text(k * 2, (TTC.iloc[0::2, :3].to_numpy())[k, 0], '%d' % (TTC.iloc[0::2, :3].to_numpy())[k, 0], ha='center',va='top')) for k in range(len(TTC.iloc[0::2, 2].to_numpy()))]
    plt.xticks(rotation=30)
    #plt.tight_layout(1.3)
    plt.savefig(os.path.join(DataFolder, h[0] + '_TTC.png'))
    plt.close()
    Data.to_csv(os.path.join(DataFolder, h[0] + '_TTC_specific.csv'), encoding='utf_8_sig', index=False)
    TTC.to_csv(os.path.join(DataFolder, h[0] + '_TTC.csv'), encoding='utf_8_sig')
    












