import os
import numpy as np
import pandas as pd
import shutil

pd.set_option('expand_frame_repr',False)


DataFolder = r'F:\01Cplusplus\01.Tired\Result\Case2\2.9.9'
videoFolder = r'F:\01Cplusplus\01.Tired\Data_select'

path_result = os.path.join(DataFolder,'Result')
if os.path.exists(path_result):
    shutil.rmtree(path_result)
os.makedirs(path_result)



with open(os.path.join(DataFolder,'version.txt')) as f:
    version = f.readline().split('\n')[0]
    print(version)

df_alarm = pd.read_csv(os.path.join(DataFolder,'alarm.csv'),encoding='utf_8_sig')
df_alarm = df_alarm.groupby(by=['Alarm','DMS result','Video Name','Mode']).agg(
    {
        'Alarm':np.min,
        'DMS result':np.min,
        'Video Name':np.min,
        'Mode':np.min,
        'alarm':lambda x:[item for item in x ]
    }
).reset_index(drop=True)
print(df_alarm)

df_TestCases = pd.read_csv(os.path.join(DataFolder,'TiredTestCases.csv'),encoding='utf_8_sig')
print(df_TestCases)

shutil.move(os.path.join(DataFolder,'version.txt'),os.path.join(path_result,'version.txt'))
shutil.move(os.path.join(DataFolder,'alarm.csv'),os.path.join(path_result,'alarm.csv'))
shutil.move(os.path.join(DataFolder,'TiredTestCases.csv'),os.path.join(path_result,'TiredTestCases.csv'))
shutil.move(os.path.join(DataFolder,'fps.csv'),os.path.join(path_result,'fps.csv'))


df_result = pd.merge(df_TestCases,df_alarm,how='left',on=['Alarm','DMS result','Video Name','Mode']).drop(['Video Path'],axis=1)



df_Alarm_missing = df_result[((df_result['DMS result']=='right')|(df_result['DMS result']=='missing'))&(df_result.apply(lambda x:True if pd.isna(np.sum(x['alarm'])) else False,axis=1))].assign(result='missing')
df_Alarm_right = df_result[((df_result['DMS result']=='right')|(df_result['DMS result']=='missing'))&(df_result.apply(lambda x:x['Alarm'] in x['alarm'] if pd.notna(np.sum(x['alarm'])) else False,axis=1))].assign(result='right')
df_Alarm_wrong = df_result[((df_result['DMS result']=='right')|(df_result['DMS result']=='missing'))&(df_result.apply(lambda x:x['Alarm'] not in x['alarm'] if pd.notna(np.sum(x['alarm'])) else False,axis=1))].assign(result='wrong')

df_NoAlarm_right = df_result[(df_result['DMS result']=='wrong')&(df_result.apply(lambda x:True if pd.isna(np.sum(x['alarm'])) else (x['Alarm'] not in x['alarm']),axis=1))].assign(result='right')
df_NoAlarm_wrong = df_result[(df_result['DMS result']=='wrong')&(df_result.apply(lambda x:False if pd.isna(np.sum(x['alarm'])) else (x['Alarm']  in x['alarm']),axis=1))].assign(result='wrong')

df_result=pd.concat([df_Alarm_wrong,df_NoAlarm_wrong,df_Alarm_missing,df_Alarm_right,df_NoAlarm_right],ignore_index=True)
print(df_result)
df_result.to_csv(os.path.join(path_result,'Result_details.csv'),index=False,encoding='utf_8_sig')

df_stat_now = df_result.groupby(['Alarm','result'])[['Video Name']].count()
#print(df_stat_now)
#print(df_stat_now.loc[[(207,'missing')],'Video Name'])




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
        [alarm, version+'版本算法', total, right, missing, wrong, '%.3f%%' % (right / total * 100) if total > 0 else 0,
         '%.3f%%' % (missing / total * 100 if total > 0 else 0), '%.3f%%' % (wrong / total * 100 if total > 0 else 0)])
print(result)
#df_alarm['result'] = df_alarm
result = np.array(result)
df_stat = pd.DataFrame(result[:,2:],index=[result[:,0],result[:,1]],columns=['用例总数','正报','漏报','误报','正报百分比','漏报百分比','误报百分比'])
print(df_stat)
df_stat.to_csv(os.path.join(path_result,'Result_stat.csv'),encoding='utf_8_sig')

