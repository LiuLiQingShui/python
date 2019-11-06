import pandas as pd
import numpy as np
import struct
import time
import os

timestart = time.time()

pd.set_option('expand_frame_repr',False)

typemap = {'U8':'B',
           'S8':'b',
           'U16':'H',
           'S16':'h',
           'U32':'I',
           'S32':'i',
           'float':'f',
           }

typeLength = {'B':1,
           'b':1,
           'H':2,
           'h':2,
           'I':4,
           'i':4,
           'f':4,
           }


def format_unpack(format):
    format_struct = format
    replacelist = list(set(format.split()))
    for item in replacelist:
        format_struct = format_struct.replace(item,typemap[item])
    format_struct = format_struct.replace(" ", '')
    return format_struct

def formatLength(format):
    formatLength = 0
    for k in format:
        formatLength = formatLength+typeLength[k]
    return formatLength


def getProtocol():
    df_protocol_sub = pd.read_csv('USB protocol_sub.csv',encoding='utf_8_sig')
    df_protocol = pd.read_csv('USB protocol.csv',encoding='utf_8_sig')
    df_protocol = df_protocol.fillna(0)
    protocol = {}
    for item in df_protocol.index:
        df_protocol_row = df_protocol.loc[item]
        protocol_value = []
        sub_list = []
        if df_protocol_row['Sub number']:
            subnumber = (df_protocol_row['Sub number']).split()
            sub = (df_protocol_row['Sub list']).split()
            for k in range(len(sub)):
                df_protocol_sub_row = df_protocol_sub[df_protocol_sub['TypeHeader']==sub[k]].iloc[0]
                sub_list.append([subnumber[k],df_protocol_sub_row['Variable Names'],format_unpack(df_protocol_sub_row['format'])])
        protocol[df_protocol_row['TypeHeader']]=[df_protocol_row['Variable Names'],format_unpack(df_protocol_row['format']),sub_list]
    return protocol


def praseInfo(DataFolder,filename):
    print('--------------------------------------------------------------------------------------')
    print('Start paring',os.path.join(DataFolder,filename))
    print('--------------------------------------------------------------------------------------')
    protocol = getProtocol()
    rawDatadict = {}
    for key in protocol.keys():
        rawDatadict[key] = []
    infofile_path = os.path.join(DataFolder,filename)
    with open(infofile_path, 'rb+') as f:
        bytesData = f.read()
    bytesData_len = len(bytesData)
    index = 0
    USBframeIndex = 0
    while index + 8 <= bytesData_len:
        TypeHeader = (struct.unpack_from('4s', bytesData[index:index + 4], 0)[0]).decode('ascii')
        DataLength = struct.unpack_from('I', bytesData[index + 4:index + 8], 0)[0]
        if TypeHeader == 'VINF':
            USBframeIndex = USBframeIndex + 1
            if (USBframeIndex % 10000) == 1:
                print(USBframeIndex)
        if DataLength > 0:
            Data = bytesData[index + 8:index + 8 + DataLength]
            if TypeHeader in rawDatadict:
                rawDatadict[TypeHeader].append([USBframeIndex, Data])
        index = index + 8 + DataLength

    outDatadict = {}
    outHeaderDict = {}
    for key in rawDatadict.keys():
        value = rawDatadict[key]
        if len(value) > 0:
            outDatadict[key] = []
            protocol_item = protocol[key]
            if len(protocol_item[2]) == 0:
                outHeaderDict[key] = [['USBframeIndex'], (protocol_item[0]).split(), []]
                format = protocol_item[1]
                for k in range(len(value)):
                    outDatadict[key].append([value[k][0]] + list(struct.unpack_from(format, value[k][1], 0)))
            elif len(protocol_item[2]) > 0:
                header_parent = protocol_item[0]
                format_parent = protocol_item[1]
                header_sub = protocol_item[2][0][1]
                format_sub = protocol_item[2][0][2]
                numberID = protocol_item[2][0][0]
                outHeaderDict[key] = [['USBframeIndex'], header_parent.split(), header_sub.split()]
                formatLength_parent = formatLength(format_parent)
                formatLength_sub = formatLength(format_sub)
                for k in range(len(value)):
                    parent_data = list(struct.unpack_from(format_parent, value[k][1], 0))
                    sub_data_num = parent_data[header_parent.split().index(numberID)]
                    if sub_data_num == 0:
                        sub_data = [np.nan] * len(format_sub)
                        outDatadict[key].append([value[k][0]] + parent_data + sub_data)
                    elif sub_data_num > 0:
                        for k_sub in range(sub_data_num):
                            sub_data = list(struct.unpack_from(format_sub, value[k][1],
                                                               formatLength_parent + formatLength_sub * k_sub))
                            outDatadict[key].append([value[k][0]] + parent_data + sub_data)

    fileID = filename.split('.')[0]
    df = pd.DataFrame(np.array(outDatadict['VINF']),
                      columns=(outHeaderDict['VINF'][0] + outHeaderDict['VINF'][1] + outHeaderDict['VINF'][2]))
    df_index = df[['USBframeIndex', 'frame_index', 'timestamp']]
    df = df[['frame_index', 'timestamp', 'type', 'format', 'reserved', 'width', 'height']]
    df.to_csv(os.path.join(DataFolder,fileID+"_VINF.csv"), index=False, encoding='utf_8_sig')
    dtypes_USBframeIndex = df_index['USBframeIndex'].dtypes
    for key in outDatadict.keys():
        if key != 'VINF':
            df = pd.DataFrame(np.array(outDatadict[key]),
                              columns=(outHeaderDict[key][0] + outHeaderDict[key][1] + outHeaderDict[key][2]))
            df["USBframeIndex"] = df["USBframeIndex"].astype(dtypes_USBframeIndex)
            df = pd.merge(df_index, df, on=['USBframeIndex'], how='outer', sort=False)
            nan_pozition = ~(df['frame_index'] == (df['frame_index'].rolling(window=2).mean()))
            df[['frame_index', 'timestamp'] + outHeaderDict[key][1]] = df[
                ['frame_index', 'timestamp'] + outHeaderDict[key][1]].where(nan_pozition, np.nan)
            df = df.drop('USBframeIndex', axis=1)
            print(df.head(5))
            df.to_csv(os.path.join(DataFolder,fileID+"_"+key+".csv"), index=False, encoding='utf_8_sig')

    timeend = time.time()
    print('--------------------------------------------------------------------------------------')
    print('paring finished')
    print("Using time:", timeend - timestart)
    print('--------------------------------------------------------------------------------------')
