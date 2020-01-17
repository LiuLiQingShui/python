import subprocess
import logging
import os
import shutil
import numpy as np
import pandas as pd
import submodule_01_getTestCase,submodule_02_collectResult,submodule_03_analysisResult,submodule_04_UpdateLDWparam


Path_LDWdetect = r'F:\LDW'
Path_TestCase = r'F:\TestCase'
resultfolder= 'Result0'

TestStep={
    'getTestCase':0,
    'clip test':0,
    'collectResult clip':0,
    'analysisResult clip':1,
    'get missing video':1,
    '3min test':1,
    'CombineClipAndThreeMinRetest':1

}

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=os.path.join(Path_TestCase,'testlog.log'),
                filemode='w')

if TestStep['getTestCase']:
    # 生成测试用例，拷贝到测试程序目录
    logging.info(r'生成测试用例，拷贝到测试程序目录：开始')
    os.chdir(Path_TestCase)
    submodule_01_getTestCase.getTestCase(Path_TestCase)
    shutil.copy(os.path.join(Path_TestCase, 'fold.txt'), os.path.join(Path_LDWdetect, 'fold.txt'))
    shutil.copy(os.path.join(Path_TestCase, 'TestCase.txt'), os.path.join(Path_LDWdetect, 'TestCase.txt'))
    logging.info(r'生成测试用例，拷贝到测试程序目录：完成')

if TestStep['clip test']:
    #运行clip测试
    logging.info(r'运行clip测试：开始')
    os.chdir(Path_LDWdetect)
    df_configure = pd.read_csv(os.path.join(Path_LDWdetect, 'configure.ini'), encoding='utf_8_sig', header=None)
    df_configure.iloc[0, 1] = 2
    df_configure.iloc[1, 1] = 10
    print(df_configure)
    df_configure.to_csv(os.path.join(Path_LDWdetect, 'configure.ini'), encoding='utf_8_sig', header=False, index=False)
    LDWTestProc = subprocess.Popen(r'LDWdetect.exe')
    LDWTestProc.wait()
    logging.info(r'运行clip测试：完成')


if TestStep['collectResult clip']:
    # 收集运行结果
    logging.info(r'收集clip运行结果：开始')
    os.chdir(Path_TestCase)
    shutil.copy(os.path.join(Path_LDWdetect,'fold.txt'),os.path.join(Path_TestCase,'fold.txt'))
    shutil.copy(os.path.join(Path_LDWdetect,'TestCase.txt'),os.path.join(Path_TestCase,'TestCase.txt'))
    resultfolder = submodule_02_collectResult.collectResult(Path_TestCase)
    logging.info(r'收集clip运行结果：结束')




#分析片段测试结果
if TestStep['analysisResult clip']:
    logging.info(r'分析片段测试结果：开始')
    submodule_03_analysisResult.analysisResult(Path_TestCase,resultfolder)
    logging.info(r'分析片段测试结果：结束')


# 得到missing视频集合
#过滤出Miss用例，用于整段重新测试（3min,recheck）
if TestStep['get missing video']:
    if not submodule_03_analysisResult.ThreeMinRetest(Path_TestCase, resultfolder):
        exit()
    shutil.copy(os.path.join(os.path.join(Path_TestCase, resultfolder), 'Recheckvideolist.csv'),
                os.path.join(Path_LDWdetect, 'Recheckvideolist.csv'))


#运行3min测试
if TestStep['3min test']:
    logging.info(r'运行3min测试：开始')
    os.chdir(Path_LDWdetect)
    df_configure = pd.read_csv(os.path.join(Path_LDWdetect, 'configure.ini'), encoding='utf_8_sig', header=None)
    df_configure.iloc[0, 1] = 3
    df_configure.iloc[1, 1] = 10
    print(df_configure)
    df_configure.to_csv(os.path.join(Path_LDWdetect, 'configure.ini'), encoding='utf_8_sig', header=False,
                        index=False)
    LDWTestProc = subprocess.Popen(r'LDWdetect.exe')
    LDWTestProc.wait()
    logging.info(r'运行3min测试：完成')


#分析合并测试结果
if TestStep['CombineClipAndThreeMinRetest']:
    logging.info(r'分析合并测试结果：开始')
    shutil.copy(os.path.join(Path_LDWdetect, 'alarm_csv.csv'),
                os.path.join(os.path.join(Path_TestCase, resultfolder), 'Retest_alarm.csv'))
    submodule_03_analysisResult.CombineClipAndThreeMinRetest(Path_TestCase, resultfolder)
    submodule_03_analysisResult.stat(os.path.join(Path_TestCase, resultfolder), 'TestResult_Recheck_detail.csv')
    logging.info(r'分析合并测试结果：结束')

