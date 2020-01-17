import os
import shutil
import numpy as np
import pandas as pd

pd.set_option('expand_frame_repr',False)

DataFolder = os.getcwd()
videoFolder = r'F:\01Cplusplus\01.Tired\Data_select'
tmep = r'/home/jimu140/Documents/samba/V1.0/build'

path_result = os.path.join(DataFolder,'Result')
if os.path.exists(path_result):
    shutil.rmtree(path_result)
os.makedirs(path_result)

ResultPaths =[
    r'F:\01Cplusplus\01.Tired\Result\Case2\2.9.9\Result_repeat3s_V1',
    r'F:\01Cplusplus\01.Tired\Result\Case2\2.9.9\Result_repeat3s_V2',
    r'F:\01Cplusplus\01.Tired\Result\Case2\2.9.9\Result_V1',
    r'F:\01Cplusplus\01.Tired\Result\Case2\2.9.9\Result_repeat3s_V3',
]

if len(ResultPaths)<2:
    print('Results less than 2, do not need to do')
    exit()

ResultInCommon = pd.read_csv(os.path.join(ResultPaths[0],'Result_details.csv'),encoding='utf_8_sig',usecols=['Alarm','DMS result','Video Name','Mode','result'])
for k in range(1,len(ResultPaths)):
    ResultSecond = pd.read_csv(os.path.join(ResultPaths[k],'Result_details.csv'),encoding='utf_8_sig',usecols=['Alarm','DMS result','Video Name','Mode','result'])
    ResultInCommon = pd.merge(ResultInCommon,ResultSecond,how='inner',on=['Alarm','DMS result','Video Name','Mode','result'])

print(ResultInCommon)
ResultInCommon.to_csv(os.path.join(path_result,'ResultInCommon.csv'),index=False,encoding='utf_8_sig')

df_TestCases = ResultInCommon[['Alarm','DMS result','Video Name','Mode']]
df_TestCases['Video Path'] = df_TestCases.apply(lambda x:tmep+'/Data_select/'+str(x['Alarm'])+'/'+str(x['DMS result'])+'/'+str(x['Video Name']),axis=1)
df_TestCases.to_csv(os.path.join(path_result,'TiredTestCases.csv'),index=False,encoding='utf_8_sig')


df_result = ResultInCommon
alarm_set = set(list(df_result['Alarm']))
print(alarm_set)

result = []
for alarm in alarm_set:
    path_alarm = os.path.join(path_result,str(alarm))
    os.makedirs((path_alarm))
    path_missing = os.path.join(path_alarm, 'missing')
    os.makedirs((path_missing))
    path_wrong = os.path.join(path_alarm, 'wrong')
    os.makedirs(path_wrong)
    df_alarm = df_result[(df_result['Alarm']==alarm)]
    df_alarm_missing = df_alarm[df_alarm['result']=='missing'].reset_index(drop=True)
    for k in range(len(df_alarm_missing)):
        videopath = os.path.join(videoFolder,str(df_alarm_missing.loc[k,'Alarm']),df_alarm_missing.loc[k,'DMS result'],df_alarm_missing.loc[k,'Video Name'])
        newvideopath = os.path.join(path_missing,df_alarm_missing.loc[k,'Video Name'])
        shutil.copy(videopath,newvideopath)
    df_alarm_wrong = df_alarm[df_alarm['result']=='wrong'].reset_index(drop=True)
    for k in range(len(df_alarm_wrong)):
        videopath = os.path.join(videoFolder,str(df_alarm_wrong.loc[k,'Alarm']),df_alarm_wrong.loc[k,'DMS result'],df_alarm_wrong.loc[k,'Video Name'])
        newvideopath = os.path.join(path_wrong,df_alarm_wrong.loc[k,'Video Name'])
        shutil.copy(videopath,newvideopath)

    total,right,wrong,missing = len(df_result[(df_result['Alarm']==alarm)]),len(df_result[(df_result['Alarm']==alarm)&(df_result['DMS result']=='right')]),len(df_result[(df_result['Alarm']==alarm)&(df_result['DMS result']=='wrong')]),len(df_result[(df_result['Alarm']==alarm)&(df_result['DMS result']=='missing')])
    result.append([alarm,'DMS result',total,right,missing,wrong,'%.3f%%'%(right/total*100) if total>0 else 0,'%.3f%%'%(missing/total*100 if total>0 else 0),'%.3f%%'%(wrong/total*100 if total>0 else 0)])
    total, right, wrong, missing = len(df_result[(df_result['Alarm'] == alarm)]), len(
        df_result[(df_result['Alarm'] == alarm) & (df_result['result'] == 'right')]), len(
        df_result[(df_result['Alarm'] == alarm) & (df_result['result'] == 'wrong')]), len(
        df_result[(df_result['Alarm'] == alarm) & (df_result['result'] == 'missing')])
    result.append(
        [alarm, '版本算法', total, right, missing, wrong, '%.3f%%' % (right / total * 100) if total > 0 else 0,
         '%.3f%%' % (missing / total * 100 if total > 0 else 0), '%.3f%%' % (wrong / total * 100 if total > 0 else 0)])
print(result)
#df_alarm['result'] = df_alarm
result = np.array(result)
df_stat = pd.DataFrame(result[:,2:],index=[result[:,0],result[:,1]],columns=['用例总数','正报','漏报','误报','正报百分比','漏报百分比','误报百分比'])
print(df_stat)
df_stat.to_csv(os.path.join(path_result,'ResultInCommon_stat.csv'),encoding='utf_8_sig')
