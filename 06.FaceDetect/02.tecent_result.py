import pandas as pd
import json
import numpy as np


'''

tecent_result_file = r'F:/101.test/CelebA/jimu/anary/tecent_result_2019-11-01 09-45-03.json'
data_tecent = []
with open(tecent_result_file) as f:
    lines = list(f.readlines())
    for line in lines:
        item = json.loads(line)
        key = list(item.keys())[0]
        if item[key]['ret'] == 0:
            nose_x = item[key]['data']['face_shape_list'][0]['nose'][0]['x']
            nose_y = item[key]['data']['face_shape_list'][0]['nose'][0]['y']
        else:
            nose_x = -1
            nose_y = -1
        data_tecent.append([key, item[key]['ret'], nose_x, nose_y])
print(data_tecent)
df_tecent = pd.DataFrame(data_tecent,columns=['picname','ret','nose_x','nose_y'])
df_tecent.to_csv('df_tecent.csv',index=False,encoding='utf_8_sig')



df_base = pd.read_csv(r'F:/101.test/CelebA/Anno/list_landmarks_celeba.txt',header=1,sep=r'\s+',index_col=0,usecols=['nose_x','nose_y'])
df_base.insert(0,'picname',df_base.index)
df_base.to_csv('df_base.csv',index=False,encoding='utf_8_sig')


df_tecent = pd.read_csv('df_tecent.csv',encoding='utf_8_sig')
print(df_tecent.head(5))
df_base = pd.read_csv('df_base.csv',encoding='utf_8_sig')
print(df_base.head(5))


df_result = pd.merge(df_tecent,df_base,on='picname',how='left',suffixes=['_tecent','_base'])
print(df_result.head(5))
df_result.to_csv('result_tecent.csv',index=False,encoding='utf_8_sig')
'''
df_result = pd.read_csv('result_tecent.csv',encoding='utf_8_sig')
print(df_result.head(5))
print(df_result.count())


right_condition = ((df_result['ret']==0)&(np.abs(df_result['nose_x_tecent']-df_result['nose_x_base'])<=10)&(np.abs(df_result['nose_y_tecent']-df_result['nose_y_base'])<=10))
print(len(right_condition),np.count_nonzero(right_condition),1-np.count_nonzero(right_condition)/len(right_condition))

stat = df_result.groupby('ret').count()
print(stat)
print(stat.loc[0,'picname'],np.sum(stat['picname']),1-stat.loc[0,'picname']/np.sum(stat['picname']))
