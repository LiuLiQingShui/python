import os
import numpy as np
import pandas as pd

#DataFolder = os.getcwd()
DataFolder = r'F:\01Cplusplus\01.Tired\Data_select'

TestCases=[]

tmep = r'/home/jimu140/Documents/samba/V1.0/build'
#tmep = r'.'
for file in os.listdir(DataFolder):
    #print(file)
    AlarmFolder = os.path.join(DataFolder,file)
    if os.path.isdir(AlarmFolder):
        categroges = ['right','wrong','missing']
        #categroges = [ 'wrong', 'missing']
        for item in categroges:
            if os.path.isdir(os.path.join(AlarmFolder,item)):
                casefolder = os.path.join(AlarmFolder,item)
                for file_casefolder in os.listdir(casefolder):
                    if file_casefolder.split('.')[-1]=='mp4':
                        #TestCases.append([file,item,file_casefolder,'0',os.path.join(casefolder,file_casefolder)])
                        TestCases.append([file, item, file_casefolder, '0', tmep+'/Data_select/'+file+'/'+item+'/'+ file_casefolder])
print(TestCases)
df_TestCases = pd.DataFrame(TestCases,columns=['Alarm','DMS result','Video Name','Mode','Video Path'])
df_TestCases.to_csv(os.path.join(DataFolder,'TiredTestCases.csv'),index=False,encoding='utf_8_sig')


