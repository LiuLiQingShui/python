import os
import time
import re
import infopraser
import draw



DataFolder = os.path.join(os.getcwd(),'Data')
#DataFolder= r'F:/00.python/02.ClientInfoPrase/Data/20190817165458'

if not os.path.exists(DataFolder):
    os.makedirs(DataFolder)

for parent, dirnames, filenames in os.walk(DataFolder):
    for filename in filenames:
        if not os.path.exists(os.path.join(DataFolder,filename)):
            continue
        if '.info' in filename:
            h = (re.split('.info', filename))[0]
            #InfoPrase_UsbDataProcess.UsbDataProcess(DataFolder, filename,h)
            draw.draw(DataFolder, h)
    for dirname in dirnames:
        #break
        subDataFolderL2 = os.path.join(DataFolder,dirname)
        for parentL2,dirnamesL2,filenamesL2 in os.walk(subDataFolderL2):
            for filenameL2 in filenamesL2:
                if '.info' in filenameL2:
                    h = (re.split('.info', filenameL2))[0]
                    #InfoPrase_UsbDataProcess.UsbDataProcess(subDataFolderL2, filenameL2,h)
                    draw.draw(subDataFolderL2,h)





