import os
import re
import CalcAllV2
import CanBinDataProcessV3
import analyseData2


#DataFolder = os.path.join(os.getcwd(),'Data')
DataFolder = os.path.join(r'F:\100.client\00.AnalyseBin\Data')
#DataFolder = os.path.join(r'F:/00.python/01.CanPrase/dist/00.AnalyseBin/Data')
#DataFolder = os.path.join(r'F:/00.python/01.CanBinPrase/dist/AdasCanDataPrase - 副本 - 副本 (3)/backup')

if not os.path.exists(DataFolder):
    os.makedirs(DataFolder)

findLaber = ['.bin','.dat']
for FindLaber in findLaber:
    for parent, dirnames, filenames in os.walk(DataFolder):
        for filename in filenames:
            if filename.find(FindLaber) >= 0:
                h = re.split(FindLaber, filename)
                #CanBinDataProcessV2.CanBinDataProcess(DataFolder, filename)
                analyseData2.analyseData(DataFolder,filename)
        for dirname in dirnames:
            # break
            subDataFolderL2 = os.path.join(DataFolder, dirname)
            for parentL2, dirnamesL2, filenamesL2 in os.walk(subDataFolderL2):
                for filenameL2 in filenamesL2:
                    if filenamesL2.find(FindLaber) >= 0:
                        h = re.split(FindLaber, filenamesL2)
                        #CanBinDataProcessV2.CanBinDataProcess(subDataFolderL2, filenamesL2)
                        analyseData2.analyseData(subDataFolderL2, filenamesL2)


#CalcAllV2.CalcAll(DataFolder)
print("\n\n")
print("ALL bins have been parsed!")
