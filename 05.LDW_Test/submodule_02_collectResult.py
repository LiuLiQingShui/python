import os
import numpy as np
import pandas as pd
import cv2
import shutil


def collectResult(DataFolder):
    pd.set_option('expand_frame_repr', False)
    count = 0
    while 1:
        try:
            resultfolder = 'Result' + str(count)
            path_result = os.path.join(DataFolder, resultfolder)
            if os.path.exists(path_result):
                print(shutil.rmtree(path_result))
            os.makedirs(path_result)
            break
        except:
            print(path_result+' is occupied')
            count = count+1
            continue
    path_detail = os.path.join(path_result, 'detail')
    os.makedirs(path_detail)
    path_detail_pic = os.path.join(path_result, 'detailpic')
    os.makedirs(path_detail_pic)
    movelist = ['.png', '_test.csv', '_foe.csv']
    copylist = ['alarm_csv', 'fps_csv', 'except.csv', 'LDWparam.csv', 'situation.txt']

    if not os.path.exists(os.path.join(DataFolder, 'TestCase.txt')):
        print(os.path.exists(os.path.join(DataFolder, 'TestCase.txt'))+' is not exit')
        return None
    with open(os.path.join(DataFolder, 'TestCase.txt'), 'r') as f:
        TestCases = list(f.readlines())
        print(TestCases)
        for item in TestCases:
            if item.split():
                case = item.split()[0]
            else:
                continue
            DataFolder_case = os.path.join(DataFolder, case)
            # 统计每一个case的结果
            if os.path.exists(os.path.join(DataFolder_case, 'except.csv')) and os.path.exists(
                    os.path.join(DataFolder_case, 'alarm_csv.csv')):
                path_detail_onecase = os.path.join(path_detail, case)
                os.makedirs(path_detail_onecase)
                path_detail_pic_onecase = os.path.join(path_detail_pic, case)
                os.makedirs(path_detail_pic_onecase)
                for parent_path_detail_onecase, dirs_path_detail_onecase, files_path_detail_onecase in os.walk(
                        DataFolder_case):
                    for item in files_path_detail_onecase:
                        for tag in movelist:
                            if tag in item:
                                shutil.move(os.path.join(DataFolder_case, item),
                                            os.path.join(path_detail_pic_onecase, item))
                        for tag in copylist:
                            if tag in item:
                                shutil.copy(os.path.join(DataFolder_case, item),
                                            os.path.join(path_detail_onecase, item))
    if os.path.exists(os.path.join(DataFolder, 'TestCase.txt')):
        shutil.move(os.path.join(DataFolder, 'TestCase.txt'), os.path.join(path_result, 'TestCase.txt'))
    if os.path.exists(os.path.join(DataFolder, 'fold.txt')):
        shutil.move(os.path.join(DataFolder, 'fold.txt'), os.path.join(path_result, 'fold.txt'))
    if os.path.exists(os.path.join(DataFolder, 'version.txt')):
        shutil.move(os.path.join(DataFolder, 'version.txt'), os.path.join(path_result, 'version.txt'))

    return resultfolder

if __name__ == '__main__':
    DataFolder = os.getcwd()
    # DataFolder = r'F:\TestCase'
    collectResult(DataFolder)
