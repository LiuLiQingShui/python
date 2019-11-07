import os
import infopraserV2
import JimuVsRadarV1
import time



DataFolder = os.path.join(os.getcwd(),'Data')
#DataFolder= r'F:/00.python/02.ClientInfoPrase/Data/20190817165458'

if not os.path.exists(DataFolder):
    os.makedirs(DataFolder)

for parent, dirnames, filenames in os.walk(DataFolder):
    for filename in filenames:
        if not os.path.exists(os.path.join(DataFolder,filename)):
            continue
        if '.info' in filename:
            JimuVsRadarV1.JimuVsRadar(DataFolder,filename)
    for dirname in dirnames:
        #break
        subDataFolderL2 = os.path.join(DataFolder,dirname)
        for parentL2,dirnamesL2,filenamesL2 in os.walk(subDataFolderL2):
            for filenameL2 in filenamesL2:
                if '.info' in filenameL2:
                    JimuVsRadarV1.JimuVsRadar(subDataFolderL2, filenameL2)

print('\n\n\n所有数据统计完毕！')

time.sleep(6000)




