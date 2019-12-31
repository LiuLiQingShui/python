import os
import numpy as np
import pandas as pd
import cv2
import shutil

pd.set_option('expand_frame_repr',False)

#DataFolder =os.getcwd()
DataFolder = r'F:\TestCase'
path_result = os.path.join(DataFolder,'Result')
path_missing = os.path.join(path_result,'missing')
os.makedirs((path_missing))
path_wrong = os.path.join(path_result,'wrong')
os.makedirs(path_wrong)
path_right = os.path.join(path_result,'right')
os.makedirs(path_right)
path_detail = os.path.join(path_result,'detail')
path_detail_pic = os.path.join(path_result,'detailpic')


df_allCasesResult = pd.DataFrame()

#把TestCase中包含的case的测试结果统计出来
with open(os.path.join(path_result,'TestCase.txt'),'r') as f:
    TestCases = list(f.readlines())
    print(TestCases)
    for item in TestCases:
        if item.split():
            case = item.split()[0]
        else:
            continue
        DataFolder_case = os.path.join(path_detail,case)
        #统计每一个case的结果
        if os.path.exists(os.path.join(DataFolder_case,'except.csv')) and os.path.exists(os.path.join(DataFolder_case,'alarm_csv.csv')):
            df_except = pd.read_csv(os.path.join(DataFolder_case,'except.csv'), encoding='utf_8_sig',usecols=['video name','frame index','alarm','former test result'])
            df_except['start'] = df_except['frame index'] - 30
            df_except['end'] = df_except['frame index'] + 30
            df_alarm = pd.read_csv(os.path.join(DataFolder_case,'alarm_csv.csv'), encoding='utf_8_sig',
                                   usecols=['video name', 'frame index', 'LDW state']).rename(columns={'frame index':'output frame index'})
            df_alarm['video name'] = df_alarm['video name'].apply(lambda x: x.strip().split('\\')[-1])
            df_result = pd.merge(df_except, df_alarm, how='left', on='video name')
            df_result = df_result[((df_result['alarm']!=0)& (((df_result['frame index'] - 30) <= df_result['output frame index']) & ((df_result['frame index'] + 30) >= df_result['output frame index'])))|((df_result['alarm']==0)& (((df_result['frame index'] - 10) <= df_result['output frame index']) & ((df_result['frame index'] + 10) >= df_result['output frame index'])))]
            df_result = df_result.groupby(['video name', 'frame index']).agg(
                {
                    'video name': np.min,
                    'frame index': np.min,
                    'alarm': np.min,
                    'former test result':np.min,
                    'LDW state': lambda x: [item for item in x],
                }
            ).reset_index(drop=True)
            df_result = pd.merge(df_except[['video name', 'frame index','alarm','former test result']], df_result[['video name',  'frame index', 'LDW state']], how='left',
                                  on=['video name', 'frame index'])
            df_videopath = df_except[['video name','frame index']]
            df_videopath['video path'] = df_videopath['video name'].apply(lambda x:os.path.join(os.path.join(DataFolder,case),x))
            print(df_videopath)
            df_result = pd.merge(df_videopath,df_result,on=['video name','frame index'],how='outer')
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
            #把单次结果累积到总的结果中
            df_allCasesResult = pd.concat([df_allCasesResult,df_caseresult])


print(df_allCasesResult)

#把结果图片分类整理
df_missing = df_allCasesResult[df_allCasesResult['result']=='missing'].reset_index(drop=True)
for k in range(len(df_missing)):
    cap = cv2.VideoCapture(df_missing.loc[k,'video path'])
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_POS_FRAMES,df_missing.loc[k,'frame index'])
        ret,frame = cap.read()
        if ret:
            picname = str(df_missing.loc[k,'TestCase'])+'_'+str(df_missing.loc[k,'video name'])+'_'+str(df_missing.loc[k,'frame index'])+'.png'
            cv2.imwrite(os.path.join(path_missing,picname),frame)

df_wrong = df_allCasesResult[df_allCasesResult['result']=='wrong'].reset_index(drop=True)
for k in range(len(df_wrong)):
    cap = cv2.VideoCapture(df_wrong.loc[k,'video path'])
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_POS_FRAMES,df_wrong.loc[k,'frame index'])
        ret,frame = cap.read()
        if ret:
            picname = str(df_wrong.loc[k,'TestCase'])+'_'+str(df_wrong.loc[k,'video name'])+'_'+str(df_wrong.loc[k,'frame index'])+'.png'
            cv2.imwrite(os.path.join(path_wrong,picname),frame)

df_right = df_allCasesResult[df_allCasesResult['result']=='right'].reset_index(drop=True)
for k in range(len(df_right)):
    cap = cv2.VideoCapture(df_right.loc[k,'video path'])
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_POS_FRAMES,df_right.loc[k,'frame index'])
        ret,frame = cap.read()
        if ret:
            picname = str(df_right.loc[k,'TestCase'])+'_'+str(df_right.loc[k,'video name'])+'_'+str(df_right.loc[k,'frame index'])+'.png'
            cv2.imwrite(os.path.join(path_right,picname),frame)

#保存测试详细结果
df_allCasesResult.to_csv(os.path.join(path_result,'TestResult_detail.csv'),index=False,encoding='utf_8_sig')


#保存统计数据
result =[]
df_stat = df_allCasesResult
total,right,missing,wrong = len(df_stat),len(df_stat[df_stat['former test result']=='right']),len(df_stat[df_stat['former test result']=='missing']),len(df_stat[df_stat['former test result']=='wrong'])
#print(total,right,missing,wrong)
result.append([total,right,missing,wrong,'%.3f%%'%(right/total*100) if total>0 else 0,'%.3f%%'%(missing/total*100 if total>0 else 0),'%.3f%%'%(wrong/total*100 if total>0 else 0)])
df_stat = df_allCasesResult
total,right,missing,wrong = len(df_stat),len(df_stat[df_stat['result']=='right']),len(df_stat[df_stat['result']=='missing']),len(df_stat[df_stat['result']=='wrong'])
#print(total,right,missing,wrong)
result.append([total,right,missing,wrong,'%.3f%%'%(right/total*100) if total>0 else 0,'%.3f%%'%(missing/total*100 if total>0 else 0),'%.3f%%'%(wrong/total*100 if total>0 else 0)])

df_stat = df_allCasesResult[df_allCasesResult['former test result']=='right']
total,right,missing,wrong = len(df_stat),len(df_stat[df_stat['result']=='right']),len(df_stat[df_stat['result']=='missing']),len(df_stat[df_stat['result']=='wrong'])
#result.append([total,right,missing,wrong,'%.3f%%'%(right/total*100) if total>0 else 0,'%.3f%%'%(missing/total*100 if total>0 else 0),'%.3f%%'%(wrong/total*100 if total>0 else 0)])
df_stat = df_allCasesResult[df_allCasesResult['former test result']=='missing']
total,right,missing,wrong = len(df_stat),len(df_stat[df_stat['result']=='right']),len(df_stat[df_stat['result']=='missing']),len(df_stat[df_stat['result']=='wrong'])
#result.append([total,right,missing,wrong,'%.3f%%'%(right/total*100) if total>0 else 0,'%.3f%%'%(missing/total*100 if total>0 else 0),'%.3f%%'%(wrong/total*100 if total>0 else 0)])
df_stat = df_allCasesResult[df_allCasesResult['former test result']=='wrong']
total,right,missing,wrong = len(df_stat),len(df_stat[df_stat['result']=='right']),len(df_stat[df_stat['result']=='missing']),len(df_stat[df_stat['result']=='wrong'])
#result.append([total,right,missing,wrong,'%.3f%%'%(right/total*100) if total>0 else 0,'%.3f%%'%(missing/total*100 if total>0 else 0),'%.3f%%'%(wrong/total*100 if total>0 else 0)])

with open(os.path.join(path_result,'version.txt')) as f:
    version = f.readline()
    version = version.split(',')
    version = version[0]+'('+version[1]+')'
result = pd.DataFrame(np.array(result).T,index=['用例数','正确','漏报','误报','正确百分比','漏报百分比','误报百分比'],columns=['历史路测结果',version+'测试结果'])
print(result)
result.to_csv(os.path.join(path_result,'TestResult_summary.csv'),encoding='utf_8_sig')
