import csv
import numpy as np

def getAdasCanProtocol(filename):
    CanProtocal = {}
    with open(filename) as f:
        reader = csv.reader(f)
        content = list(reader)
        dict=[]
        dataStart = 0
        for row in content:
            if row[0]=='START':
                dataStart = 1
                continue
            if row[0] == 'END':
                dataStart = 0
                if len(dict)>3:
                    Protocal = (np.array(dict[2:(len(dict))]))[:,:8]
                    selectname = Protocal[:,:1]
                    selectname=list(selectname.reshape(len(selectname)))
                    #print(Protocal, selectname)

                    fullname=[]
                    fmt=[]
                    data =[]
                    Protocal = np.insert(Protocal,0,['0', '0', '0' ,'0' ,'0' ,'0' ,'0', '0'],axis=0)
                    Protocal = np.insert(Protocal, len(Protocal), ['0', '64', '0', '0', '0', '0', '0', '0'], axis=0)
                    #Protocal = Protocal.tolist()

                    for i in range(0,len(Protocal)-1):
                        if (int(Protocal[i,1])+int(Protocal[i,2]))<int(Protocal[i+1,1]):
                            name = 'unused_' + str(i)
                            #print(int(Protocal[i, 1]),int(Protocal[i, 2]), int(Protocal[i + 1, 1]),int(Protocal[i + 1, 1]) - int(Protocal[i, 1])-int(Protocal[i, 2]))
                            data_row = [int(Protocal[i, 1])+int(Protocal[i, 2]), int(Protocal[i + 1, 1]) - int(Protocal[i, 1])-int(Protocal[i, 2]), 0, 0, 0, 1]
                            fmtrow = 'uintle:' + str(data_row[1])
                            fullname.append(name)
                            data.append(data_row)
                            fmt.append(fmtrow)
                            if i < (len(Protocal) - 2):
                                fullname.append(Protocal[i + 1, 0])
                                data.append(list(Protocal[i + 1, 1:7]))
                                fmt.append(Protocal[i + 1, 7] + ":" + Protocal[i + 1, 2])
                        else:
                            if i==(len(Protocal)-2):
                                1
                            else:
                                fullname.append(Protocal[i + 1, 0])
                                data.append(list(Protocal[i + 1, 1:7]))
                                #print(Protocal[i + 1, 1:7])
                                fmt.append(Protocal[i + 1, 7] + ":" + Protocal[i + 1, 2])
                    data = np.array(data).astype(float)
                    Protocal = [fullname,data,fmt,selectname]
                    CanProtocal[dict[0][1]]=Protocal
                    if dict[0][1]=='0x7b0':
                        temp = ['0x7b1','0x7b2','0x7b3','0x7b4','0x7b5','0x7b6','0x7b7','0x7b8','0x7b9','0x7ba','0x7bb','0x7bc','0x7bd','0x7be','0x7bf']
                        for k in temp:
                            CanProtocal[k] = Protocal
                dict = []
                continue
            if dataStart:
                dict.append(row)
        return CanProtocal


