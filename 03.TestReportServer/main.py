import os
import re
import CanBinDataProcessV2
import time
import analyseData2



#DataFolder = os.path.join(os.getcwd(),'Data')
#DataFolder = os.path.join(r'F:/00.Python/03.TestReportServer/bin')
#analyseData2.analyseData(DataFolder,'20190815195702.bin',["cccc","ddddd"])

a = ['光照-白天', '光照-傍晚', '光照-黑夜', '天气-晴', '天气-雨', '天气-雪', '天气-阴', '天气-沙尘暴', '天气-雾', '路况-市内', '路况-高速', '路况-国道', '路况-县道']
b = ['光照-白天',  '光照-黑夜',  '路况-市内', '路况-高速', '路况-国道', '路况-县道']

dict = {}
#dict['光照'] = 1
for x in a:
    t = x.split("-")
    if t[0] not in dict:
        dict[t[0]] = [t[1]]
    else:
        attt = dict[t[0]]
        attt.append(t[1])
        dict[t[0]] = attt

print(dict)

findlaber = 1
for key,value in dict.items():
    findlaber_sub = 0
    for t in value:
        if (key+'-'+t ) in b:
            findlaber_sub=1
            break;
    if  findlaber_sub==0:
        findlaber = 0
        break

print(findlaber)
