import csv

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
                    CanProtocal[dict[0][1]]=dict[2:(len(dict))]
                    if dict[0][1]=='0x7b0':
                        temp = ['0x7b1','0x7b2','0x7b3','0x7b4','0x7b5','0x7b6','0x7b7','0x7b8','0x7b9','0x7ba','0x7bb','0x7bc','0x7bd','0x7be','0x7bf']
                        for k in temp:
                            CanProtocal[k] = dict[2:(len(dict))]
                dict = []
                continue
            if dataStart:
                dict.append(row)
        return CanProtocal


