import os,stat
import shutil

count = 1
resultlist = [
    'alarm.csv',
    'fps.csv',
    'TiredTestCases.csv',
    'version.txt',
    '01.getTiredTestCase.pyw'
]

while count:
    resultpath = os.path.join(os.getcwd(),'Result_{:04}'.format(count))
    if os.path.exists(resultpath):
        count = count +1
        continue
    os.mkdir(resultpath)
    #os.chmod(resultpath,stat.S_IRWXO)
    for item in os.listdir(os.getcwd()):
        if os.path.isfile(item):
            print(os.path.basename(item))
            if os.path.basename(item) in resultlist:
                #print('''aaaa''')
                #pass
                shutil.copy(item,resultpath)
    break