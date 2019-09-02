import os
import re
import CanBinDataProcessV2
import time
import analyseData_Test



#DataFolder = os.path.join(os.getcwd(),'Data')
DataFolder = os.path.join(r'F:/test/1')
#DataFolder = os.path.join(r'F:/00.python/01.CanBinPrase/dist/AdasCanDataPrase - 副本 - 副本 (3)/backup')

if not os.path.exists(DataFolder):
    os.makedirs(DataFolder)

FindLaber = '.bin'

for parent, dirnames, filenames in os.walk(DataFolder):
    for filename in filenames:
        if filename.find(FindLaber) >= 0:
            h = re.split(FindLaber, filename)
            #CanBinDataProcessV2.CanBinDataProcess(DataFolder,filename)
            analyseData_Test.analyseData(DataFolder,filename)

#CalcAllV2.CalcAll(DataFolder)
print("\n\n")
print("ALL bins have been parsed!")
