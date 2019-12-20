import pandas as pd
import numpy as np
import time
import os
import shutil

bbox_file = r'F:/101.test/CelebA/Anno/list_bbox_celeba.txt'
landmarks_file = r'F:/101.test/CelebA/Anno/list_landmarks_celeba.txt'

bbox_jimu_file = r'F:/101.test/CelebA/jimu/bbox.csv'

bbox_testresult_file = r'F:/101.test/CelebA/jimu/bbox_testresult.csv'
landmarks_testresult_file = r'F:/101.test/CelebA/jimu/landmarks_testresult.csv'
pic_path = r'F:/101.test/CelebA/jimu/pic'
pic_notfound_path = r'F:/101.test/CelebA/jimu/pic_notfound'
pic_wrong_path = r'F:/101.test/CelebA/jimu/pic_wrong'


landmarks_thread = 10

timestart = time.time()


'''
df_base = pd.read_csv(r'F:/101.test/CelebA/Anno/list_bbox_celeba.txt',header=1,sep=r'\s+',usecols=['image_id','width','height'])
df_base = df_base.rename(columns={'image_id':'picname'})
df_base.to_csv('df_base_bbox.csv',index=False,encoding='utf_8_sig')
print(df_base.head(5))

bbox = pd.read_csv('df_base_bbox.csv',encoding='utf_8_sig')
print(bbox.head(5))
size_little_than60 = bbox[~((bbox['width']>=60)&(bbox['height']>=60))]['picname'].to_numpy().tolist()


nothandlepic_file = r'F:/101.test/CelebA/jimu/nothandlepic.csv'
df_jimu_notfound = pd.read_csv(nothandlepic_file)
df_jimu_notfound['ret'] = -1
df_jimu_notfound['nose_x'] = -1
df_jimu_notfound['nose_y'] = -1
df_jimu_notfound = df_jimu_notfound[['picname','ret','nose_x','nose_y']]
print(df_jimu_notfound.head(5))
print(len(df_jimu_notfound))
landmarks_jimu_file = r'F:/101.test/CelebA/jimu/landmarks.csv'
df_jimu = pd.read_csv(landmarks_jimu_file)
df_jimu[['x1','x2','x3','x4','x5',]] = df_jimu[['x1','x2','x3','x4','x5',]] - np.tile(df_jimu[['h_t']].to_numpy(),(1,5))
df_jimu[['y1','y2','y3','y4','y5']] =df_jimu[['y1','y2','y3','y4','y5']] -np.tile(df_jimu[['v_t']].to_numpy(),(1,5))
df_jimu = df_jimu[['picname','x5','y5']]
df_jimu = df_jimu.rename(columns={'x5':'nose_x','y5':'nose_y'})
df_jimu.insert(1,'ret',0)
print(df_jimu.head(5))
print(len(df_jimu))
df_jimu= pd.concat([df_jimu,df_jimu_notfound],0)
df_jimu = df_jimu[~df_jimu['picname'].isin(size_little_than60)]

print(df_jimu.head(5))
print(len(df_jimu))
df_jimu.to_csv('df_jimu.csv',index=False,encoding='utf_8_sig')



df_base = pd.read_csv('df_base.csv',encoding='utf_8_sig')
print(df_base.head(5))

df_jimu=pd.read_csv('df_jimu.csv',encoding='utf_8_sig')
print(df_jimu.head(5))

df_result = pd.merge(df_jimu,df_base,on='picname',how='left',suffixes=['_jimu','_base'])
print(df_result.head(5))
df_result.to_csv('result_jimu.csv',index=False,encoding='utf_8_sig')
'''


df_result = pd.read_csv('result_jimu.csv',encoding='utf_8_sig')
print(df_result.head(5))
print(df_result.count())


right_condition = ((df_result['ret']==0)&(np.abs(df_result['nose_x_jimu']-df_result['nose_x_base'])<=10)&(np.abs(df_result['nose_y_jimu']-df_result['nose_y_base'])<=10))
print(len(right_condition),np.count_nonzero(right_condition),1-np.count_nonzero(right_condition)/len(right_condition))

stat = df_result.groupby('ret').count()
print(stat)
print(stat.loc[0,'picname']/np.sum(stat['picname']),1-stat.loc[0,'picname']/np.sum(stat['picname']))

