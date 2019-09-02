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
                dict = []
                continue
            if dataStart:
                dict.append(row)
        return CanProtocal


