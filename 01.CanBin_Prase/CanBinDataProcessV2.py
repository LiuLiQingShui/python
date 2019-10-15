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
def get_s16(val):
    if val < 0x8000:
        return val
    else:
        return (val - 0x10000)


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
    notinclude=[]

    objs = []
    lines = []
    obj = []
    line = []
    count_obj = 0
    count_line= 0
    Oringe=[]
    linesmobileye = []
    linemobileye=[]
    count_linemobileye=0
    while data:
        data = f.read(16)
        try:
            b1 = struct.unpack('LL8B', data)
            #print(b1)
        except:
            print("Finish!")
            break
        dt_now = dt_base * 1000 + b1[0]
        ID = hex(b1[1])
        #print(b1)
        #print(b1[2:])
        Oringe.append([dt_now,b1[0],ID, ''.join([(('%#04x ' % k)[2:].upper()) for k in b1[2:]])])
        #print([dt_now,b1[0],ID, ''.join([(('%#04x ' % k)[2:].upper()) for k in b1[2:]])])
        if CanProtocal.get(ID):
            protocol_select = CanProtocal.get(ID)
            testdata = bitstring.BitArray('')
            for j in range(9, 1, -1):
                nn1 = int(b1[j])
                b1_hex_partion = '%#04x' % nn1
                #print(b1_hex_partion)
                testdata.append(b1_hex_partion)
            #print(testdata)
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
                if  ((int(protocol_partion[2]))%8)==0 and ID =='0xa0':
                    bitarray_temp1 = bitstring.BitArray(uintle=block.uint, length=int(protocol_partion[2]))
                    blockvalue = bitarray_temp1.uint * (float(protocol_partion[6])) + float(protocol_partion[3])
                else:
                    if (ID== '0x766' or ID== '0x768') and protocol_partion[0]=='c0':
                        blockvalue = get_s16(block.uint)* (float(protocol_partion[6])) + float(protocol_partion[3])
                    else:
                        blockvalue = block.uint * (float(protocol_partion[6])) + float(protocol_partion[3])
                data_dict.append(blockvalue)
            if ID in data_prase:
                t = (data_prase[ID])
                t.append(data_dict)
                data_prase[ID]=(t)
            else:
                data_prase[ID] = [data_dict]

            if ID>='0x7b0' and ID<='0x7bf':
                if count_obj ==0:
                    obj =obj+data_dict
                    dt_obj = dt_now
                elif (dt_now - dt_obj)<=10:
                    obj =obj+data_dict
                else:
                    objs.append(obj)
                    obj=[]
                    obj = obj + data_dict
                    dt_obj = dt_now
                count_obj=count_obj+1

            if ID >= '0x79a' and ID <= '0x79d':
                if count_line== 0:
                    line = line + data_dict
                    dt_line = dt_now
                elif (dt_now - dt_line) <= 10:
                    line = line + data_dict
                else:
                    lines.append(line)
                    line = []
                    line = line + data_dict
                    dt_line = dt_now
                count_line= count_line + 1

            if ID >= '0x766' and ID <= '0x769':
                if count_linemobileye== 0:
                    linemobileye = linemobileye + data_dict
                    dt_linemobileye = dt_now
                elif (dt_now - dt_linemobileye) <= 5:
                    linemobileye = linemobileye + data_dict
                else:
                    linesmobileye.append(linemobileye)
                    linemobileye = []
                    linemobileye = linemobileye + data_dict
                    dt_linemobileye = dt_now
                count_linemobileye= count_linemobileye + 1
        else:
            notinclude.append(ID)

    h=re.split('.bin|.dat', filename)
    for key,value in data_prase.items():
        protocol_select = CanProtocal.get(key)
        protocol_select = np.array(protocol_select)
        columnsName = ['时间','timestamp','Can ID']+list(protocol_select[:,0])
        df = pd.DataFrame(value,columns=columnsName)
        print(df.dtypes)
        csv_filename = os.path.join(DataFolder, h[0] +'_'+key+ '_testresult.csv')
        df.to_csv(csv_filename,encoding='utf_8_sig',index=False)

    protocol_select = CanProtocal.get('0x7b0')
    protocol_select = np.array(protocol_select)
    columnsNameobj = (['时间', 'timestamp', 'Can ID'] + list(protocol_select[:, 0])) * 16
    df1 = pd.DataFrame(objs)
    df = pd.DataFrame(objs, columns=columnsNameobj[0:df1.shape[1]])
    print(df.dtypes)
    csv_filename = os.path.join(DataFolder, h[0] + '_objs_testresult.csv')
    df.to_csv(csv_filename, encoding='utf_8_sig', index=False)

    columnsNameLine = []
    for k in ['0x79a', '0x79b', '0x79c', '0x79d']:
        protocol_select = CanProtocal.get(k)
        protocol_select = np.array(protocol_select)
        columnsName = ['时间', 'timestamp', 'Can ID'] + list(protocol_select[:, 0])
        columnsNameLine = columnsNameLine + columnsName
    df1 = pd.DataFrame(lines)
    df = pd.DataFrame(lines, columns=columnsNameLine[0:df1.shape[1]])
    print(df.dtypes)
    csv_filename = os.path.join(DataFolder, h[0] + '_lines_testresult.csv')
    df.to_csv(csv_filename, encoding='utf_8_sig', index=False)


    df = pd.DataFrame(linesmobileye)
    print(df.dtypes)
    csv_filename = os.path.join(DataFolder, h[0] + '_linesmobileye_testresult.csv')
    df.to_csv(csv_filename, encoding='utf_8_sig', index=False)

    df = pd.DataFrame(Oringe, columns=['time','index','ID','Data'])
    print(df.dtypes)
    csv_filename = os.path.join(DataFolder, h[0] + '_Oringe_testresult.csv')
    df.to_csv(csv_filename, encoding='utf_8_sig', index=False)
    #Oringe.append([dt_now, b1[0], ID, ''.join([str(k, encoding="utf-8") for k in b1[2:]])])
    print("notinclude:",notinclude)



