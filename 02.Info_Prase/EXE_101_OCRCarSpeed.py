import os
import re
import time
from pathlib import Path
import numpy as np
import cv2
import pytesseract
import PIL
import pandas as pd

def takeSecond(elem):
    return elem[1]

def ORCText(picpath):
    image = cv2.imread(picpath)
    image = image[0:30, :]
    image = PIL.Image.fromarray(image)
    image = image.convert('L')
    text = pytesseract.image_to_string(image, lang='eng')
    return text

def OCRCarSpeed(DataFolder,timeperiod):
    #print(DataFolder)
    FindLaber = '.jpg'
    picName = []
    for parent, dirnames, filenames in os.walk(DataFolder):
        for filename in filenames:
            if filename.find(FindLaber) >= 0:
                h = re.split('.jpg|_', filename)
                #print(h)
                picName.append([int(h[0]),int(h[1])])
    picName.sort(key=takeSecond)
    Data = pd.DataFrame(columns=['Frameindex', 'PicName', 'Speed','OrangeSpeed'])
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    timeperiod = pd.read_csv(timeperiod)
    for kkkk in range(len(timeperiod)):
        frameperiod = [timeperiod.iloc[kkkk,0], timeperiod.iloc[kkkk,1]]
        Datalist = []
        for i in range(len(picName)):
            print(picName[i][1])
            if picName[i][1] < frameperiod[0]:
                continue
            if picName[i][1] > frameperiod[1]:
                break
            picname = str(picName[i][0]) + "_" + str(picName[i][1]) + ".jpg"
            picpath = os.path.join(DataFolder, picname)
            text = ORCText(picpath)
            speed_re = np.nan
            Obj = re.search('%.*/H', text)
            if Obj:
                #print(Obj.group())
                Obj = re.search("\s*[0-9a-zA-Z]*/H", Obj.group())
                if (Obj):
                    Obj = Obj.group()
                    #print(Obj)
                    if len(Obj)<=8:
                        Obj = re.sub('[Oo]', '0', Obj, count=0, flags=0)
                        Obj = re.sub('[Ss]', '5', Obj, count=0, flags=0)
                        Obj = re.sub('[Zz]', '2', Obj, count=0, flags=0)
                        Obj = re.sub('[LlIi]', '1', Obj, count=0, flags=0)
                        Obj = re.sub('[Tt]', '7', Obj, count=0, flags=0)
                        Obj = re.match("\s*\d+", Obj)
                        #print(Obj)
                        if Obj:
                            speed_re = re.sub(r'\D', "", Obj.group())
                            if len(speed_re)>0:
                                if float(speed_re)<120:
                                    speed_re = float(speed_re)
            Datalist.append([picName[i][1], picname, speed_re])
            #print(text)
            #print([picName[i][1], picname, speed_re])
        Data_temp = pd.DataFrame(Datalist, columns=['Frameindex', 'PicName', 'Speed'])
        SSS = pd.Series(Data_temp['Speed'])
        Data_temp.insert(3, 'OrangeSpeed', SSS)
        #print(Data_temp.dtypes)
        #print(Data_temp.head(30))
        if len(Data_temp)>0:
            #print()
            Data_temp.iloc[0, 2] = (Data_temp[Data_temp['Speed'] > 0]).iloc[0, 2]
        Data_temp['Speed'].interpolate(inplace=True)
        Data = pd.concat([Data,Data_temp])
    Data.to_csv( os.path.join(DataFolder, 'Data2.csv'),index=False)


picfolder= r"F:/99.client/01.processInfo_20190820/Data/20190815201318"
timeperiod =r"F:/99.client/01.processInfo_20190820/Data/20190815201318/timeperiod.csv"
OCRCarSpeed(picfolder,timeperiod)








