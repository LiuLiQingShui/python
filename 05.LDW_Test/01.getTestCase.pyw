import os
import cv2

DataFolder =os.getcwd()
#DataFolder= r'F:/100.client/01.processInfo_20190820/Data'
with open('fold.txt','w') as f:
    f.write(DataFolder)

TestCases = []
videos = []
for parent, dirnames, filenames in os.walk(DataFolder):
    for dirname in dirnames:
        try:
            case = int(dirname)
            TestCases.append(dirname)
            DataFolder_sub1 = os.path.join(DataFolder,dirname)
            for parent_sub1, dirnames_sub1, filenames_sub1 in os.walk(DataFolder_sub1):
                for filename_sub1 in filenames_sub1:
                    if not os.path.exists(os.path.join(DataFolder_sub1, filename_sub1)):
                        continue
                    if '.ts' in filename_sub1:
                        videos.append(filename_sub1)
                videos.sort()
                with open(os.path.join(DataFolder_sub1, 'videolist.txt'), 'w') as f:
                    for item in videos:
                        f.write(item)
                        f.write('\n')
                videos.clear()
        except:
            continue



with open(os.path.join(DataFolder,'TestCase.txt'),'w') as f:
    for item in TestCases:
        f.write(item)
        f.write('\n')




