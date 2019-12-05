import os
import numpy as np
import pandas as pd
import cv2

pd.set_option('expand_frame_repr',False)

DataFolder =os.getcwd()
df_allCasesResult = pd.DataFrame()
with open('TestCase.txt','r') as f:
    TestCases = list(f.readlines())
    print(TestCases)
    for item in TestCases:
        if item.split():
            case = item.split()[0]
        else:
            continue
        DataFolder_case = os.path.join(DataFolder,case)
        if os.path.exists(os.path.join(DataFolder_case,'except.csv')) and os.path.exists(os.path.join(DataFolder_case,'alarm_csv.csv')):
            df_except = pd.read_csv(os.path.join(DataFolder_case,'except.csv'), encoding='utf_8_sig',usecols=['video name','frame index','alarm','former test result'])
            df_except['start'] = df_except['frame index'] - 30
            df_except['end'] = df_except['frame index'] + 30
            df_alarm = pd.read_csv(os.path.join(DataFolder_case,'alarm_csv.csv'), encoding='utf_8_sig',
                                   usecols=['video name', 'frame index', 'LDW state']).rename(columns={'frame index':'output frame index'})
            df_alarm['video name'] = df_alarm['video name'].apply(lambda x: x.strip().split('\\')[-1])
            df_alarm['video path'] = df_alarm['video name'].apply(lambda x:os.path.join(DataFolder_case,x))
            df_result = pd.merge(df_except, df_alarm, how='left', on='video name')
            df_result = df_result[
                (df_result['start'] <= df_result['output frame index']) & (df_result['end'] >= df_result['output frame index'])]
            df_result = df_result.groupby(['video name', 'frame index']).agg(
                {
                    'video name': np.min,
                    'frame index': np.min,
                    'alarm': np.min,
                    'former test result':np.min,
                    'LDW state': lambda x: [item for item in x],
                }
            ).reset_index(drop=True)
            df_result = pd.merge(df_except[['video name', 'frame index','alarm','former test result']], df_result[['video name', 'frame index', 'LDW state']], how='left',
                                  on=['video name', 'frame index'])
            df_result.insert(0, 'TestCase', case)
            #print(df_result)
            df_NoAlarm_right = df_result[(pd.isna(df_result['LDW state']))&(df_result['alarm']==0)].assign(result='right')
            df_NoAlarm_wrong = df_result[(~pd.isna(df_result['LDW state'])) & (df_result['alarm'] == 0)].assign(result='wrong')
            df_Alarm_missing = df_result[(pd.isna(df_result['LDW state']))&(df_result['alarm']!=0)].assign(result='missing')

            df_alarm_RightAndWrong = df_result[(~pd.isna(df_result['LDW state']))&(df_result['alarm']!=0)]
            df_Alarm_right =df_alarm_RightAndWrong[(df_alarm_RightAndWrong.apply(lambda x: x['alarm'] in x['LDW state'] , axis=1))].assign(result='right')
            df_Alarm_wrong = df_alarm_RightAndWrong[(~df_alarm_RightAndWrong.apply(lambda x: x['alarm'] in x['LDW state'] , axis=1))].assign(result='wrong')

            df_caseresult = pd.concat([df_Alarm_missing,df_Alarm_wrong,df_NoAlarm_wrong,df_Alarm_right, df_NoAlarm_right], sort=False).reset_index(drop=True)
            #print(df_caseresult)
            df_allCasesResult = pd.concat([df_allCasesResult,df_caseresult])

#df_allCasesResult = df_allCasesResult.drop(['time'],axis=1)
print(df_allCasesResult)
df_allCasesResult.to_csv('TestResult_detail.csv',index=False,encoding='utf_8_sig')

result =[]

df_stat = df_allCasesResult
total,right,missing,wrong = len(df_stat),len(df_stat[df_stat['result']=='right']),len(df_stat[df_stat['result']=='missing']),len(df_stat[df_stat['result']=='wrong'])
#print(total,right,missing,wrong)
result.append(['历史总数',total,right,missing,wrong,'%.3f'%(right/total*100) if total>0 else 0,'%.3f'%(missing/total*100 if total>0 else 0),'%.3f'%(wrong/total*100 if total>0 else 0)])



df_stat = df_allCasesResult[df_allCasesResult['former test result']=='right']
total,right,missing,wrong = len(df_stat),len(df_stat[df_stat['result']=='right']),len(df_stat[df_stat['result']=='missing']),len(df_stat[df_stat['result']=='wrong'])
#print(total,right,missing,wrong)
result.append(['历史正确',total,right,missing,wrong,'%.3f'%(right/total*100) if total>0 else 0,'%.3f'%(missing/total*100 if total>0 else 0),'%.3f'%(wrong/total*100 if total>0 else 0)])

df_stat = df_allCasesResult[df_allCasesResult['former test result']=='missing']
total,right,missing,wrong = len(df_stat),len(df_stat[df_stat['result']=='right']),len(df_stat[df_stat['result']=='missing']),len(df_stat[df_stat['result']=='wrong'])
#print(total,right,missing,wrong)
result.append(['历史漏报',total,right,missing,wrong,'%.3f'%(right/total*100) if total>0 else 0,'%.3f'%(missing/total*100 if total>0 else 0),'%.3f'%(wrong/total*100 if total>0 else 0)])


df_stat = df_allCasesResult[df_allCasesResult['former test result']=='wrong']
total,right,missing,wrong = len(df_stat),len(df_stat[df_stat['result']=='right']),len(df_stat[df_stat['result']=='missing']),len(df_stat[df_stat['result']=='wrong'])
#print(total,right,missing,wrong)
result.append(['历史误报',total,right,missing,wrong,'%.3f'%(right/total*100) if total>0 else 0,'%.3f'%(missing/total*100 if total>0 else 0),'%.3f'%(wrong/total*100 if total>0 else 0)])

#print(result)
result = pd.DataFrame(result,columns=['用例','用例数','测试结果-正确','测试结果-漏报','测试结果-误报','测试结果-正确百分比','测试结果-漏报百分比','测试结果-误报百分比'])
print(result)
result.to_csv('TestResult_summary.csv',index=False,encoding='utf_8_sig')


#print(df_allCasesResult.groupby(['result','former test result']).count())

#df_allCasesResult['former test result']=='right'
#df_allCasesResult.to_csv('Result.csv',index=False,encoding='utf_8_sig')




