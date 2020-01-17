import os
import infopraserV2
import JimuVsRadarV1
import time



DataFolder = os.path.join(os.getcwd(),'Data')
#DataFolder= r'F:/00.python/02.ClientInfoPrase/Data/20190817165458'
if not os.path.exists(DataFolder):
    os.makedirs(DataFolder)

configure={}
with open('configure.ini') as f:
    lines = f.readlines()
    for item in lines:
        data = item.strip().split('=')
        if len(data) == 2:
            try:
                configure[data[0]] = float(data[1])
            except:
                continue

print(configure)
if ('mode' not in configure) or ('breakpointexit' not in configure):
    print('configure.ini中mode、breakpointexit错误，请检查后，填写正确的值')
    time.sleep(30)
    exit()

drawSpeed = 0
if 'drawSpeed' in configure:
    drawSpeed = configure['drawSpeed']

def DrawInFolder(DataFolder):
    for dir in os.listdir(DataFolder):
        path = os.path.join(DataFolder,dir)
        if os.path.isdir(path):
            DrawInFolder(path)
            continue
        if dir.split('.')[-1]=='info':
            JimuVsRadarV1.JimuVsRadar(DataFolder,dir,configure['mode'],configure['breakpointexit'],drawSpeed)


DrawInFolder(DataFolder)


print('\n\n\n所有数据统计、画图完毕！')

time.sleep(60)




