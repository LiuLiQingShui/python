import pandas as pd
import numpy as np
import os

TestResult = pd.read_csv("TestCase.csv")
alarm = pd.read_csv("alarm.csv")
fps = pd.read_csv("fps.csv")

error = alarm[alarm['frameindex']<0]
errorData = TestResult[TestResult['Videoname'].isin(error['Videoname'].tolist())]
TestResult=TestResult[~TestResult['Videoname'].isin(error['Videoname'].tolist())]
alarm=alarm[~alarm['Videoname'].isin(error['Videoname'].tolist())]

result=[]
restext = []
fps_detail = []
for k in range(len(TestResult)):
    temp = alarm[(alarm['Videoname']==TestResult.iloc[k,0]) &(alarm['mode']==TestResult.iloc[k,1])&(alarm['frameindex']>=TestResult.iloc[k,2])&(alarm['frameindex']<=TestResult.iloc[k,3])]
    #print(temp)
    res = 'Fail'
    if len(temp)==1:
        if temp.iloc[0,3]==TestResult.iloc[k,4]:
            res = 'Pass'
    result.append(res)
    texttemp  = []
    for ttt in range(len(temp)):
        texttemp.append('[')
        texttemp.append(str(temp.iloc[ttt,2]))
        texttemp.append(' ')
        texttemp.append(str(temp.iloc[ttt, 3]))
        texttemp.append(']')
    restext.append("".join(texttemp))

    start_index=-1
    end_index = -1

    fps_temp = fps[(fps['Videoname']==TestResult.iloc[k,0])]
    print(fps_temp)
    fps_temp.index=np.arange(len(fps_temp))
    print(fps_temp)

    temp = fps_temp[(fps_temp['framestart']<=TestResult.iloc[k,2])&(fps_temp['frameend']>=TestResult.iloc[k,2])].index.tolist()
    if len(temp)>0:
        start_index = (temp[0]-5) if (temp[0]-5)>0 else 0
        print((start_index))

    temp = fps_temp[(fps_temp['framestart'] <= TestResult.iloc[k, 3]) & (
                fps_temp['frameend'] >= TestResult.iloc[k, 3])].index.tolist()
    if len(temp)>0:
        end_index = temp[0]
        print((end_index))
    else:
        if start_index>=0:
            end_index = len(fps_temp)-1

    if start_index<0 or end_index<0:
        fps_detail.append("")
    else:
        str_temp =""
        for kk in range(start_index,end_index+1):
            str_temp = str_temp+ str(fps_temp.iloc[kk,1])+" "
        fps_detail.append(str_temp)
    #temp.tolist()
    #print(temp.tolist())


TestResult = TestResult.assign(Result=result,details = restext,fps_details=fps_detail)
errorData = errorData.assign(Result="用例错误",details = "用例的文件名或模式设置错误",fps_details="")
TestResult = pd.concat([TestResult,errorData],axis=0)
TestResult.to_csv('TestResult.csv', encoding='utf_8_sig', index=False)
