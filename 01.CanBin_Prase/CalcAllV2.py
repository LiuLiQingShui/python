import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def CalcAll(DataFolder):
    LDW=pd.DataFrame()
    for parent, dirnames, filenames in os.walk(DataFolder):
        for filename in filenames:
            if filename.find('_LDW.csv') >= 0:
                if len(LDW)>0:
                    LDW = LDW+pd.read_csv(os.path.join(DataFolder,filename))
                else:
                    LDW = pd.read_csv(os.path.join(DataFolder, filename))
    LDW = pd.DataFrame(LDW[['Right','Missing','Wrong']].to_numpy(),index=['Mobileye LDW左','Jimu LDW左','Mobileye LDW右','Jimu LDW右','Mobileye Total','Jimu Total'],columns=['Right','Missing','Wrong'])
    LDW = LDW.assign(Right_ratio=LDW['Right']/([(LDW['Right'].to_numpy())[k//2*2] for k in range(len(LDW['Right'].to_numpy()))]),Missing_ratio=LDW['Missing']/([(LDW['Right'].to_numpy())[k//2*2] for k in range(len(LDW['Right'].to_numpy()))]),Wrong_ratio=LDW['Wrong']/([(LDW['Right'].to_numpy())[k//2*2] for k in range(len(LDW['Right'].to_numpy()))]))
    plt.close('all')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    LDW.iloc[:,:3].plot.bar(stacked=True,figsize=(8,8),title='LDW告警对比分析：Jimu、Mobileye\n')
    [(plt.text(k*2+1, (LDW.iloc[1::2,:3].to_numpy())[k,0], '%d' % (LDW.iloc[1::2,:3].to_numpy())[k,0], ha='center', va='top'),plt.text(k*2+1, (LDW.iloc[1::2,:3].to_numpy())[k,:2].sum(), '%d' % (LDW.iloc[1::2,:3].to_numpy())[k,1], ha='center', va='top'),plt.text(k*2+1, (LDW.iloc[1::2,:3].to_numpy())[k,:3].sum(), '%d' % (LDW.iloc[1::2,:3].to_numpy())[k,2], ha='center', va='top')) for k in range(len(LDW.iloc[1::2,2].to_numpy()))]
    [(plt.text(k*2, (LDW.iloc[0::2,:3].to_numpy())[k,0], '%d' % (LDW.iloc[0::2,:3].to_numpy())[k,0], ha='center', va='top')) for k in range(len(LDW.iloc[0::2,2].to_numpy()))]
    plt.xticks(rotation=30)
    plt.savefig(os.path.join(DataFolder, '00.总计_LDW_.png'))
    plt.close()
    LDW.to_csv(os.path.join(DataFolder, '00.总计_LDW_.csv'), encoding='utf_8_sig')

    TTC=pd.DataFrame()
    for parent, dirnames, filenames in os.walk(DataFolder):
        for filename in filenames:
            if filename.find('_TTC.csv') >= 0:
                print(pd.read_csv(os.path.join(DataFolder,filename)))
                if len(TTC)>0:
                    TTC = TTC+pd.read_csv(os.path.join(DataFolder,filename))
                else:
                    TTC = pd.read_csv(os.path.join(DataFolder, filename))
    TTC = pd.DataFrame(TTC[['Right','Missing','Wrong']].to_numpy(),index=['TTC_Mobileye','TTC_Jimu'],columns=['Right','Missing','Wrong'])
    TTC = TTC.assign(Right_ratio=TTC['Right']/([(TTC['Right'].to_numpy())[k//2*2] for k in range(len(TTC['Right'].to_numpy()))]),Missing_ratio=TTC['Missing']/([(TTC['Right'].to_numpy())[k//2*2] for k in range(len(TTC['Right'].to_numpy()))]),Wrong_ratio=TTC['Wrong']/([(TTC['Right'].to_numpy())[k//2*2] for k in range(len(TTC['Right'].to_numpy()))]))
    TTC.iloc[:, :3].plot.bar(stacked=True, figsize=(8, 8),title='TTC告警对比分析：Jimu、Mobileye\n' )
    [(plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, 0], '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 0], ha='center', va='top'),plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, :2].sum(), '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 1],ha='center', va='top'), plt.text(k * 2 + 1, (TTC.iloc[1::2, :3].to_numpy())[k, :3].sum(), '%d' % (TTC.iloc[1::2, :3].to_numpy())[k, 2], ha='center',va='top')) for k in range(len(TTC.iloc[1::2, 2].to_numpy()))]
    [(plt.text(k * 2, (TTC.iloc[0::2, :3].to_numpy())[k, 0], '%d' % (TTC.iloc[0::2, :3].to_numpy())[k, 0], ha='center',va='top')) for k in range(len(TTC.iloc[0::2, 2].to_numpy()))]
    plt.xticks(rotation=30)
    plt.savefig(os.path.join(DataFolder,  '00.总计_TTC_.png'))
    plt.close()
    TTC.to_csv(os.path.join(DataFolder,  '00.总计_TTC_.csv'), encoding='utf_8_sig')


    LDW_specific=pd.DataFrame()
    for parent, dirnames, filenames in os.walk(DataFolder):
        for filename in filenames:
            if filename.find('_LDW_specific.csv') >= 0:
                if len(LDW_specific)>0:
                    LDW_specific = pd.concat([LDW_specific,pd.read_csv(os.path.join(DataFolder,filename))])
                else:
                    LDW_specific = pd.read_csv(os.path.join(DataFolder, filename))
    LDW_specific.to_csv(os.path.join(DataFolder, '00.总计_LDW_specific_.csv'), encoding='utf_8_sig', index=False)


    TTC_specific=pd.DataFrame()
    for parent, dirnames, filenames in os.walk(DataFolder):
        for filename in filenames:
            if filename.find('_TTC_specific.csv') >= 0:
                if len(TTC_specific)>0:
                    TTC_specific = pd.concat([TTC_specific,pd.read_csv(os.path.join(DataFolder,filename))])
                else:
                    TTC_specific = pd.read_csv(os.path.join(DataFolder, filename))
    TTC_specific.to_csv(os.path.join(DataFolder, '00.总计_TTC_specific_.csv'), encoding='utf_8_sig', index=False)
