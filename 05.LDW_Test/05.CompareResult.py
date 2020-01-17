import os
import numpy as np
import pandas as pd

'''
result_1 = pd.read_csv(r'F:\TestCase\ReportALLVersion\Result-4.0.14,Wed Jan  8 140819 2020\1\TestResult_Recheck_detail.csv',encoding='utf_8_sig',usecols=['TestCase','video name','frame index','alarm','former test result','道路','光照','天气','车道线','LDW state','output frame index','result'])
result_2 = pd.read_csv(r'F:\TestCase\ReportALLVersion\Result-4.0.14,Wed Jan  8 140819 2020\2\TestResult_Recheck_detail.csv',encoding='utf_8_sig',usecols=['TestCase','video name','frame index','alarm','former test result','道路','光照','天气','车道线','LDW state','output frame index','result'])
ResultCompare = pd.merge(result_1,result_2,how='outer',on=['TestCase','video name','frame index','alarm','former test result','道路','光照','天气','车道线'],suffixes=('_1','_2'))
ResultCompare.to_csv('ResultCompare.csv',encoding='utf_8_sig',index=False)
'''

result_1 = pd.read_csv(r'F:\TestCase\ReportALLVersion\Result-4.0.14,Wed Jan  8 140819 2020\1\Retest_alarm.csv',encoding='utf_8_sig',usecols=['video name','frame index','LDW state'])
result_2 = pd.read_csv(r'F:\TestCase\ReportALLVersion\Result-4.0.14,Wed Jan  8 140819 2020\2\Retest_alarm.csv',encoding='utf_8_sig',usecols=['video name','frame index','LDW state'])
result_1['video name'] = result_1['video name'].apply(lambda x:x.split('\\')[-1])
result_2['video name'] = result_2['video name'].apply(lambda x:x.split('\\')[-1])
print(result_1)
print(result_2)
ResultCompare = pd.merge(result_1,result_2,how='outer',on=['video name','frame index'],suffixes=('_1','_2'))
ResultCompare.to_csv('ResultCompare_full.csv',encoding='utf_8_sig',index=False)

# ResultCompare = ResultCompare.groupby('video name').agg(
#     {
#         'video name':np.min,
#         'LDW state_1':lambda x:[item for item in x],
# 'LDW state_2':lambda x:[item for item in x],
#     }
# ).reset_index(drop=True)
print(ResultCompare)
df_videoname_diff = ResultCompare[ResultCompare['LDW state_1']!=ResultCompare['LDW state_2']][['video name']].groupby('video name').agg(
    {
        'video name':np.min,
    }
).reset_index(drop=True)
df_videoname_common = ResultCompare[ResultCompare['LDW state_1']==ResultCompare['LDW state_2']][['video name']].groupby('video name').agg(
    {
        'video name':np.min,
    }
).reset_index(drop=True)
print(df_videoname_diff)
print(df_videoname_common)
df_videoname_twoside = pd.merge(df_videoname_diff,df_videoname_common,how='inner',on='video name')
print(df_videoname_twoside)