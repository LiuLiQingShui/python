import os
import infopraserV2
import JimuVsRadarV1
import time


DataFolder = os.path.join(os.getcwd(),'Data')
#DataFolder= r'F:/100.client/01.processInfo_20190820/Data'
if not os.path.exists(DataFolder):
    os.makedirs(DataFolder)


def praseInFolder(DataFolder):
    for dir in os.listdir(DataFolder):
        path = os.path.join(DataFolder,dir)
        if os.path.isdir(path):
            praseInFolder(path)
            continue
        if dir.split('.')[-1]=='info':
            infopraserV2.praseInfo(DataFolder,dir)


praseInFolder(DataFolder)


print('\n\n\n所有数据解析完毕！')

time.sleep(60)


