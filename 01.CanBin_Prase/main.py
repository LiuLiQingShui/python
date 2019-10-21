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
print(pro['0x700'])

fmt=pro['0x700'][2]
#print(fmt)
for i in range(len(fmt)):
    fmtspilt = re.split(':', fmt[i])
    #print(fmtspilt)


print(int('0x0000000009000000',16))

s = bitstring.ConstBitStream('0x0000000009000000')
print(s.read('uintbe:16'))
print(s.read('uintbe:16'))
print(s.read('uintle:32'))



s = bitstring.ConstBitStream('0x0000000900000000')
print(s.read('uintbe:32'))
print(s.read('uintbe:16'))
print(s.read('uintbe:16'))

s = bitstring.ConstBitStream('0x0820000101800000')
print(s.readlist(['uint:3', 'uint:13', 'uint:1', 'uint:7', 'uint:1', 'uint:7', 'uint:1', 'uint:1', 'uint:1', 'uint:1', 'uint:12', 'uint:3', 'uint:5', 'uint:2', 'uint:1', 'uint:5']))
