import pandas as pd
import json
import numpy as np

'''
faceplusplus_result_file = r'F:/101.test/CelebA/jimu/anary/faceplusplus_result_2019-11-01 11-37-25.json'
data_faceplusplus = []
with open(faceplusplus_result_file) as f:
    lines = list(f.readlines())
    for line in lines:
        item = json.loads(line)
        key = list(item.keys())[0]
        if item[key]['face_num'] > 0:
            nose_x = item[key]['faces'][0]['landmark']['nose_tip']['x']
            nose_y = item[key]['faces'][0]['landmark']['nose_tip']['y']
        else:
            nose_x = -1
            nose_y = -1
        data_faceplusplus.append([key, item[key]['face_num'], nose_x, nose_y])
print(data_faceplusplus)
df_faceplusplus = pd.DataFrame(data_faceplusplus,columns=['picname','ret','nose_x','nose_y'])
df_faceplusplus.to_csv('df_faceplusplus.csv',index=False,encoding='utf_8_sig')

'''



'''
df_base = pd.read_csv(r'F:/101.test/CelebA/Anno/list_landmarks_celeba.txt',header=1,sep=r'\s+',index_col=0,usecols=['nose_x','nose_y'])
df_base.insert(0,'picname',df_base.index)
df_base.to_csv('df_base.csv',index=False,encoding='utf_8_sig')





df_faceplusplus = pd.read_csv('df_faceplusplus.csv',encoding='utf_8_sig')
print(df_faceplusplus.head(5))
df_base = pd.read_csv('df_base.csv',encoding='utf_8_sig')
print(df_base.head(5))


df_result = pd.merge(df_faceplusplus,df_base,on='picname',how='left',suffixes=['_faceplusplus','_base'])
print(df_result.head(5))
df_result.to_csv('result_faceplusplus.csv',index=False,encoding='utf_8_sig')
'''

df_result = pd.read_csv('result_faceplusplus.csv',encoding='utf_8_sig')
print(df_result.head(5))
print(df_result.count())


right_condition = ((df_result['ret']>0)&(np.abs(df_result['nose_x_faceplusplus']-df_result['nose_x_base'])<=10)&(np.abs(df_result['nose_y_faceplusplus']-df_result['nose_y_base'])<=10))
print(len(right_condition),np.count_nonzero(right_condition),1-np.count_nonzero(right_condition)/len(right_condition))

stat = df_result.groupby('ret').count()
print(stat)
print(stat.loc[0,'picname']/np.sum(stat['picname']),1-stat.loc[0,'picname']/np.sum(stat['picname']))
'''
'''