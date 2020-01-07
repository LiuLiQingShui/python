import os
import numpy as np
import pandas as pd
import cv2
import shutil

pd.set_option('expand_frame_repr',False)

DataFolder =os.getcwd()
#DataFolder = r'F:\TestCase'
path_LDWparam = os.path.join(DataFolder,'LDWparam')
if os.path.exists(path_LDWparam):
    shutil.rmtree(path_LDWparam)
os.makedirs(path_LDWparam)


with open(os.path.join(DataFolder,'TestCase.txt'),'r') as f:
    TestCases = list(f.readlines())
    print(TestCases)
    for item in TestCases:
        if item.split():
            case = item.split()[0]
        else:
            continue
        DataFolder_case = os.path.join(DataFolder,case)
        #统计每一个case的结果
        if os.path.exists(os.path.join(DataFolder_case,'foe.csv')) and os.path.exists(os.path.join(DataFolder_case,'LDWparam.csv')):
            df_LDWparam = pd.read_csv(os.path.join(DataFolder_case,'LDWparam.csv'),encoding='utf_8_sig',usecols=['name','value'])
            df_foe = pd.read_csv(os.path.join(DataFolder_case,'foe.csv'),encoding='utf_8_sig',usecols=['vanish_pt_x','vanish_pt_y'])
            if len(df_foe)>0:
                df_LDWparam.iloc[df_LDWparam[(df_LDWparam['name']=='foe_x')].index.tolist()[0],1] = df_foe.iloc[-1,0]
                df_LDWparam.iloc[df_LDWparam[(df_LDWparam['name'] == 'foe_y')].index.tolist()[0], 1] = df_foe.iloc[
                    -1, 1]
            df_LDWparam['appdex'] = 1
            df_LDWparam.to_csv(os.path.join(DataFolder_case,'LDWparam.csv'),encoding='utf_8_sig',index=False)
            path_LDWparam_onecase = os.path.join(path_LDWparam, case)
            os.makedirs(path_LDWparam_onecase)
            shutil.copy(os.path.join(DataFolder_case,'LDWparam.csv'), os.path.join(path_LDWparam_onecase, 'LDWparam.csv'))



#保存版本号

shutil.move(os.path.join(DataFolder,'TestCase.txt'),os.path.join(path_LDWparam,'TestCase.txt'))
if os.path.exists(os.path.join(DataFolder,'fold.txt')):
    shutil.move(os.path.join(DataFolder,'fold.txt'),os.path.join(path_LDWparam,'fold.txt'))
if os.path.exists(os.path.join(DataFolder,'version.txt')):
    shutil.move(os.path.join(DataFolder,'version.txt'),os.path.join(path_LDWparam,'version.txt'))

