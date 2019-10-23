import bitstring
import struct
import time
import t_getAdasCanProtocol
import json
import re
import os
import numpy as np
import pandas as pd
import t_getAdasCanProtocol


pro = t_getAdasCanProtocol.getAdasCanProtocol('ADAS CAN protocol.csv')

#print(pro)
#print(pro.keys())
#print(pro.values())
print(pro['0x7b0'][3])
print(type(pro['0x7b0'][3]))
print(type(pro['0x7b0'][3][1]))
fmt=pro['0x7b0'][2]
#print(fmt)
for i in range(len(fmt)):
    fmtspilt = re.split(':', fmt[i])
    #print(fmtspilt)


df = pd.DataFrame(np.array([[1,1,1],[2,2,2],[3,3,3]]),columns=['a','b','c'])
print(df)
print(type(df))
print(df.dtypes)

df = df[['a','b']]
print(df)
print(type(df))
print(df.dtypes)

