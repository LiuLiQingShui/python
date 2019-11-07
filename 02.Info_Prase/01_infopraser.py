import os
import infopraserV2
import JimuVsRadarV1
import time


DataFolder = os.path.join(os.getcwd(),'Data')
#DataFolder= r'F:/100.client/01.processInfo_20190820/Data'



if not os.path.exists(DataFolder):
    os.makedirs(DataFolder)

for parent, dirnames, filenames in os.walk(DataFolder):
    for filename in filenames:
        if not os.path.exists(os.path.join(DataFolder,filename)):
            continue
        if '.info' in filename:
            infopraserV2.praseInfo(DataFolder, filename)
    for dirname in dirnames:
        subDataFolderL2 = os.path.join(DataFolder,dirname)
        for parentL2,dirnamesL2,filenamesL2 in os.walk(subDataFolderL2):
            for filenameL2 in filenamesL2:
                if '.info' in filenameL2:
                    infopraserV2.praseInfo(subDataFolderL2, filenameL2)



print('\n\n\n所有数据解析完毕！')

time.sleep(60)


