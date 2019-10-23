import bitstring
import struct
import time
import t_getAdasCanProtocol
import json
import re
import os
import numpy as np
import pandas as pd


def CanBinDataProcess(DataFolder,filename):
    BinData_Path = os.path.join(DataFolder, filename)
    print(BinData_Path)
    print("Start Processing ...........")
    f = open(BinData_Path, 'rb')
    data = f.read(32)
    b = struct.unpack('8L', data)
    time_local = time.localtime(b[0])
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    dt_base = b[0]
    print("Bin Data date:",dt)
    timestart = time.time()

    CanProtocal = t_getAdasCanProtocol.getAdasCanProtocol('ADAS CAN protocol.csv')
    Data = {}
    Protocal_ID = list(CanProtocal.keys())
    for item in Protocal_ID:
        Data[item] = []

    count = 0
    while data:
        data = f.read(8)
        try:
            b1 = struct.unpack('LL', data)
        except:
            print("Finish!")
            break
        ID = hex(b1[1])
        bytesdata = f.read(8)[::-1]
        if ID in Protocal_ID:
            Data[ID].append([b1[0],bytesdata])
            count =count+1
            if (count%100)==0:
                print(count)

    Data_prase = {}
    h = re.split('.bin|.dat', filename)
    for item in Protocal_ID:
        oneData = Data[item]
        if len(oneData) > 0:
            Data_prase[item]=[]
            fmt = CanProtocal[item][2][::-1]
            protocol = CanProtocal[item][1]
            for i in range(len(fmt)):
                fmtspilt = re.split(':', fmt[i])
                if (fmtspilt[0]=='uintle' or fmtspilt[0]=='uintbe') and (int(fmtspilt[1])%8 !=0):
                    fmt[i] = 'uint:'+fmtspilt[1]
                if (fmtspilt[0]=='intle' or fmtspilt[0]=='intbe') and (int(fmtspilt[1])%8 !=0):
                    fmt[i] = 'int:'+fmtspilt[1]
                if int(fmtspilt[1])%8 ==0:
                    if fmtspilt[0]=='intbe':
                        fmt[i] = 'intle:' + fmtspilt[1]
                    if fmtspilt[0]=='intle':
                        fmt[i] = 'intbe:' + fmtspilt[1]
                    if fmtspilt[0]=='uintle':
                        fmt[i] = 'uintbe:' + fmtspilt[1]
                    if fmtspilt[0]=='uintbe':
                        fmt[i] = 'uintle:' + fmtspilt[1]
            title = CanProtocal[item][0][::-1]
            selectname = CanProtocal[item][3]
            timestamp = []
            print(item)
            for i in range(len(oneData)):
                ConstBitStreamdata = bitstring.ConstBitStream(oneData[i][1])
                Data_prase[item].append(ConstBitStreamdata.unpack(fmt))
                timestamp.append(oneData[i][0])
            Data_prase[item] = (np.array(Data_prase[item]))*(protocol[:,5].flatten()[::-1])+(protocol[:,2].flatten()[::-1])
            df = pd.DataFrame(Data_prase[item],columns=title)
            df= df[selectname]
            dt_now = dt_base * 1000 + np.array(timestamp)
            #dt_now = dt_base * 1000 + timestamp
            df.insert(0, 'timestamp', dt_now)
            df.insert(0, '时间', pd.to_datetime(df['timestamp'].to_numpy() // 1000, unit='s', utc=True).tz_convert(
                'Asia/Shanghai'))
            csv_filename = os.path.join(DataFolder, h[0] + '_' + item + '_testresult.csv')
            df.to_csv(csv_filename, encoding='utf_8_sig', index=False)

    timeend = time.time()
    print("prase time cost:",timeend-timestart)




