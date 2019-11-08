import pandas as pd
import json
import numpy as np



'''
baidu_result_file = r'F:/101.test/CelebA/jimu/anary/baidu_result_2019-11-01 09-09-48.json'
data_baidu = []
with open(baidu_result_file) as f:
    lines = list(f.readlines())
    for line in lines:
        item = json.loads(line)
        key = list(item.keys())[0]
        if item[key]['error_code'] == 0:
            nose_x = item[key]['result']['face_list'][0]['landmark'][2]['x']
            nose_y = item[key]['result']['face_list'][0]['landmark'][2]['y']
        else:
            nose_x = -1
            nose_y = -1
        data_baidu.append([key, item[key]['error_code'], nose_x, nose_y])
print(data_baidu)
df_baidu = pd.DataFrame(data_baidu,columns=['picname','ret','nose_x','nose_y'])
df_baidu.to_csv('df_baidu.csv',index=False,encoding='utf_8_sig')
'''



'''

df_base = pd.read_csv(r'F:/101.test/CelebA/Anno/list_landmarks_celeba.txt',header=1,sep=r'\s+',index_col=0,usecols=['nose_x','nose_y'])
df_base.insert(0,'picname',df_base.index)
df_base.to_csv('df_base.csv',index=False,encoding='utf_8_sig')





df_baidu = pd.read_csv('df_baidu.csv',encoding='utf_8_sig')
print(df_baidu.head(5))
df_base = pd.read_csv('df_base.csv',encoding='utf_8_sig')
print(df_base.head(5))


df_result = pd.merge(df_baidu,df_base,on='picname',how='left',suffixes=['_baidu','_base'])
print(df_result.head(5))
df_result.to_csv('result_baidu.csv',index=False,encoding='utf_8_sig')
'''

df_result = pd.read_csv('result_baidu.csv',encoding='utf_8_sig')
print(df_result.head(5))
print(df_result.count())


right_condition = ((df_result['ret']==0)&(np.abs(df_result['nose_x_baidu']-df_result['nose_x_base'])<=10)&(np.abs(df_result['nose_y_baidu']-df_result['nose_y_base'])<=10))
print(len(right_condition),np.count_nonzero(right_condition),1-np.count_nonzero(right_condition)/len(right_condition))

stat = df_result.groupby('ret').count()
print(stat)
print(stat.loc[0,'picname'],np.sum(stat['picname']),1-stat.loc[0,'picname']/np.sum(stat['picname']))
'''
'''