import os
import cv2

DataFolder =os.getcwd()
#DataFolder= r'F:/100.client/01.processInfo_20190820/Data'
with open('fold.txt','w') as f:
    f.write(DataFolder)

TestCases = []
videos = []

for dir in os.listdir(DataFolder):
    filepath = os.path.join(DataFolder,dir)
    if os.path.isdir(filepath):
        try:
            case = int(dir)
            TestCases.append(dir)
            for file in os.listdir(filepath):
                if not os.path.exists(os.path.join(filepath,file)):
                    continue
                if '.ts' in file:
                    videos.append(file)
            videos.sort()
            with open(os.path.join(filepath, 'videolist.txt'), 'w') as f:
                for item in videos:
                    f.write(item)
                    f.write('\n')
            videos.clear()
        except:
            continue

with open(os.path.join(DataFolder, 'TestCase.txt'), 'w') as f:
    for item in TestCases:
        f.write(item)
        f.write('\n')







