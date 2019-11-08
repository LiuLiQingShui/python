import pandas as pd
import numpy as np
import time
import os
import shutil

bbox_file = r'F:/101.test/CelebA/Anno/list_bbox_celeba.txt'
landmarks_file = r'F:/101.test/CelebA/Anno/list_landmarks_celeba.txt'

bbox_jimu_file = r'F:/101.test/CelebA/jimu/bbox.csv'
landmarks_jimu_file = r'F:/101.test/CelebA/jimu/landmarks.csv'
nothandlepic_file = r'F:/101.test/CelebA/jimu/nothandlepic.csv'
bbox_testresult_file = r'F:/101.test/CelebA/jimu/bbox_testresult.csv'
landmarks_testresult_file = r'F:/101.test/CelebA/jimu/landmarks_testresult.csv'
pic_path = r'F:/101.test/CelebA/jimu/pic'
pic_notfound_path = r'F:/101.test/CelebA/jimu/pic_notfound'
pic_wrong_path = r'F:/101.test/CelebA/jimu/pic_wrong'


landmarks_thread = 10

timestart = time.time()

with open(bbox_file) as f:
    bbox = f.readlines()[2:]
    bbox = [item.split() for item in bbox]
    bbox = pd.DataFrame(np.array(bbox),columns=["picname", "x","y","width","height"])
    bbox[["x","y","width","height"]] = bbox[["x","y","width","height"]].astype(int)


with open(landmarks_file) as f:
    landmarks = f.readlines()[2:]
    landmarks = [item.split() for item in landmarks]
    landmarks = pd.DataFrame(np.array(landmarks),columns=['picname','lefteye_x', 'lefteye_y', 'righteye_x' ,'righteye_y', 'nose_x', 'nose_y', 'leftmouth_x', 'leftmouth_y', 'rightmouth_x', 'rightmouth_y'])
    landmarks[['lefteye_x', 'lefteye_y', 'righteye_x' ,'righteye_y', 'nose_x', 'nose_y', 'leftmouth_x', 'leftmouth_y', 'rightmouth_x', 'rightmouth_y']] =     landmarks[['lefteye_x', 'lefteye_y', 'righteye_x' ,'righteye_y', 'nose_x', 'nose_y', 'leftmouth_x', 'leftmouth_y', 'rightmouth_x', 'rightmouth_y']].astype(int)

bbox_jimu = pd.read_csv(bbox_jimu_file)
landmarks_jimu = pd.read_csv(landmarks_jimu_file)
nothandlepic = pd.read_csv(nothandlepic_file)

bbox_jimu[['x']] = bbox_jimu[['x']] - bbox_jimu[['h_t']].to_numpy()
bbox_jimu[['y']] = bbox_jimu[['y']] - bbox_jimu[['v_t']].to_numpy()
landmarks_jimu[['x1','x2','x3','x4','x5',]] = landmarks_jimu[['x1','x2','x3','x4','x5',]] - np.tile(landmarks_jimu[['h_t']].to_numpy(),(1,5))
landmarks_jimu[['y1','y2','y3','y4','y5']] =landmarks_jimu[['y1','y2','y3','y4','y5']] -np.tile(landmarks_jimu[['v_t']].to_numpy(),(1,5))

endpic = bbox[bbox['picname'].isin([bbox_jimu.iloc[len(bbox_jimu)-1,0]])].index.to_numpy()[0]
bbox = bbox.iloc[:endpic+1]
bbox = bbox[~bbox['picname'].isin(nothandlepic['picname'].to_numpy().tolist())]

size_little_than60 = bbox[~((bbox['width']>=60)&(bbox['height']>=60))]['picname'].to_numpy().tolist()
print('size_little_than60:',size_little_than60)

bbox_nofound = bbox[~bbox['picname'].isin(bbox_jimu['picname'].to_numpy().tolist())]
bbox_nofound = pd.merge(bbox_nofound,bbox_jimu,on='picname',how='left')
bbox_nofound.insert(1, 'result',-1)

bbox_found = bbox[bbox['picname'].isin(bbox_jimu['picname'].to_numpy().tolist())].reset_index(drop=True)
bbox_jimu = bbox_jimu.reset_index(drop=True)
right_condition = (bbox_found['x']<=bbox_jimu['x'])&(bbox_found['y']<=bbox_jimu['y'])&((bbox_found['width']+bbox_found['x'])>=bbox_jimu['width']+bbox_jimu['x'])&(bbox_found['height']+bbox_found['y']>=bbox_jimu['height']+bbox_jimu['y'])
bbox_res = pd.merge(bbox_found,bbox_jimu,on='picname',how='left')
bbox_res.insert(1, 'result',right_condition)
bbox_res[['result']] = bbox_res[['result']].astype(int)

bbox_res = pd.concat([bbox_res,bbox_nofound],axis=0).drop(['h_t','v_t'], axis=1)
bbox_res = bbox_res.rename({ 'x_y':'x_jimu',	'y_y':'y_jimu','width_y':'width_jimu','height_y':'height_jimu'}, axis='columns')
bbox_res = bbox_res[~bbox_res['picname'].isin(size_little_than60)]
bbox_res.to_csv(bbox_testresult_file, encoding='utf_8_sig', index=False)

bbox_res = bbox_res.groupby(bbox_res['result']).agg({'result': 'count'})
allcount = bbox_res.loc[-1].to_numpy()[0]+bbox_res.loc[0].to_numpy()[0]+bbox_res.loc[1].to_numpy()[0]
ratio_right = bbox_res.loc[1].to_numpy()[0]/allcount
ration_wrong = bbox_res.loc[0].to_numpy()[0]/allcount
ratio_nofoundface = bbox_res.loc[-1].to_numpy()[0]/allcount
print("BBOX ratio_right,ration_wrong,ratio_nofoundface:",ratio_right,ration_wrong,ratio_nofoundface)



endpic =  landmarks[landmarks['picname'].isin([landmarks_jimu.iloc[len(landmarks_jimu)-1,0]])].index.to_numpy()[0]
landmarks = landmarks.iloc[:endpic+1]
landmarks = landmarks[~landmarks['picname'].isin(nothandlepic['picname'].to_numpy().tolist())]

landmarks_nofound = landmarks[~landmarks['picname'].isin(landmarks_jimu['picname'].to_numpy().tolist())]
landmarks_nofound = pd.merge(landmarks_nofound,landmarks_jimu,on='picname',how='left')
landmarks_nofound.insert(1, 'result',-1)

landmarks_found = landmarks[landmarks['picname'].isin(landmarks_jimu['picname'].to_numpy().tolist())].reset_index(drop=True)
landmarks_jimu = landmarks_jimu.reset_index(drop=True)
right_condition_right_eye = ((landmarks_jimu['x1']+landmarks_jimu['x2'])/2-landmarks_found['righteye_x']<=landmarks_thread)&((landmarks_jimu['y1']+landmarks_jimu['y2'])/2-landmarks_found['righteye_y']<=landmarks_thread)
right_condition_left_eye = ((landmarks_jimu['x3']+landmarks_jimu['x4'])/2-landmarks_found['lefteye_x']<=landmarks_thread)&((landmarks_jimu['y3']+landmarks_jimu['y4'])/2-landmarks_found['lefteye_y']<=landmarks_thread)
right_condition_nose = (landmarks_jimu['x5']-landmarks_found['nose_x']<=landmarks_thread)&(landmarks_jimu['y5']-landmarks_found['nose_y']<=landmarks_thread)
right_condition = right_condition_right_eye&right_condition_left_eye&right_condition_nose
landmarks_res = pd.merge(landmarks_found,landmarks_jimu,on='picname',how='left')
landmarks_res.insert(1, 'result',right_condition)
landmarks_res[['result']] = landmarks_res[['result']].astype(int)

landmarks_res = pd.concat([landmarks_res,landmarks_nofound],axis=0).drop(['h_t','v_t','leftmouth_x', 'leftmouth_y', 'rightmouth_x', 'rightmouth_y'], axis=1)
#bbox_res = bbox_res.rename({ 'x_y':'x_jimu',	'y_y':'y_jimu','width_y':'width_jimu','height_y':'height_jimu'}, axis='columns')
landmarks_res = landmarks_res[~landmarks_res['picname'].isin(size_little_than60)]
landmarks_res.to_csv(landmarks_testresult_file, encoding='utf_8_sig', index=False)

pic_notfound = landmarks_res[landmarks_res['result']==-1]['picname'].to_numpy().tolist()
pic_wrongdetect = landmarks_res[landmarks_res['result']==0]['picname'].to_numpy().tolist()



landmarks_res = landmarks_res.groupby(landmarks_res['result']).agg({'result': 'count'})
allcount = landmarks_res.loc[-1].to_numpy()[0]+landmarks_res.loc[0].to_numpy()[0]+landmarks_res.loc[1].to_numpy()[0]
ratio_right = landmarks_res.loc[1].to_numpy()[0]/allcount
ration_wrong = landmarks_res.loc[0].to_numpy()[0]/allcount
ratio_nofoundface = landmarks_res.loc[-1].to_numpy()[0]/allcount
print("landmarks ratio_right,ration_wrong,ratio_nofoundface:",ratio_right,ration_wrong,ratio_nofoundface)

timeend = time.time()
print("Using time:",timeend-timestart)


pic_notfound = [item.split('.')[0]   for item in pic_notfound]
pic_wrongdetect = [item.split('.')[0]   for item in pic_wrongdetect]
print(pic_notfound,pic_wrongdetect)


pic_path = r'F:/101.test/CelebA/jimu/pic/dectectpic'
pic_notfound_path = r'F:/101.test/CelebA/jimu/pic_notfound'
pic_wrong_path = r'F:/101.test/CelebA/jimu/pic_wrong'

if not os.path.exists(pic_notfound_path):
    os.makedirs(pic_notfound_path)
if not os.path.exists(pic_wrong_path):
    os.makedirs(pic_wrong_path)

for parents,dirs,files in os.walk(pic_path):
    for file in files:
        laber = file.split('_')[0]
        if laber in pic_notfound:
            shutil.move(os.path.join(pic_path,file),pic_notfound_path)
        if laber in pic_wrongdetect:
            shutil.move(os.path.join(pic_path,file),pic_wrong_path)
timeend = time.time()
print("Using time:",timeend-timestart)

