import bitstring
import struct
import time
import t_getAdasCanProtocol
import json
import re
import os
import numpy as np
import pandas as pd

# -*- coding: utf-8 -*-

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
    CanProtocal = t_getAdasCanProtocol.getAdasCanProtocol('ADAS CAN protocol.csv')
    data_prase={}
    while data:
        data = f.read(16)
        try:
            b1 = struct.unpack('LL8B', data)
        except:
            print("Finish!")
            break
        dt_now = dt_base * 1000 + b1[0]
        ID = hex(b1[1])
        if CanProtocal.get(ID):
            protocol_select = CanProtocal.get(ID)
            testdata = bitstring.BitArray('')
            for j in range(9, 1, -1):
                nn1 = int(b1[j])
                b1_hex_partion = '%#04x' % nn1
                testdata.append(b1_hex_partion)
            xxx = '0b' + '{:064b}'.format(testdata.uint)
            testdata_bin = bitstring.BitArray(xxx)
            time_local = time.localtime(int(dt_now/1000))
            dt_show = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            print(dt_show)
            print(ID)
            data_dict = [dt_show,dt_now,ID]
            for i in range(len(protocol_select)):
                protocol_partion = protocol_select[i]
                block = testdata_bin[
                        (64 - int(protocol_partion[1]) - int(protocol_partion[2])):(64 - int(protocol_partion[1]))]
                if  ((int(protocol_partion[2]))%8)==0:
                    bitarray_temp1 = bitstring.BitArray(uintle=block.uint, length=int(protocol_partion[2]))
                    blockvalue = bitarray_temp1.uint * (float(protocol_partion[6])) + float(protocol_partion[3])
                else:
                    blockvalue = block.uint * (float(protocol_partion[6])) + float(protocol_partion[3])
                data_dict.append(blockvalue)
            if ID in data_prase:
                t = (data_prase[ID])
                t.append(data_dict)
                data_prase[ID]=(t)
            else:
                data_prase[ID] = [data_dict]
    h = re.split('.bin', filename)
    for key,value in data_prase.items():
        protocol_select = CanProtocal.get(key)
        protocol_select = np.array(protocol_select)
        columnsName = ['时间','timestamp','Can ID']+list(protocol_select[:,0])
        df = pd.DataFrame(value,columns=columnsName)
        print(df.dtypes)
        csv_filename = os.path.join(DataFolder, h[0] +'_'+key+ '_testresult.csv')
        df.to_csv(csv_filename,encoding='utf_8_sig',index=False)





