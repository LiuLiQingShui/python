import os
import re
import CalcAllV2
import CanBinDataProcessV2
import analyseData2


DataFolder = os.path.join(os.getcwd(),'Data')
#DataFolder = os.path.join(r'F:/test/1')
#DataFolder = os.path.join(r'F:/00.python/01.CanBinPrase/dist/AdasCanDataPrase - 副本 - 副本 (3)/backup')

if not os.path.exists(DataFolder):
    os.makedirs(DataFolder)



CalcAllV2.CalcAll(DataFolder)
print("\n\n")
print("Calculating Finished!")
