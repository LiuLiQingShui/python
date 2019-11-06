import pandas as pd
import numpy as np
from io import StringIO,BytesIO
import time
import datetime


import pytz


df2 = pd.DataFrame({'a': ['one', 'one', 'two', 'two', 'two', 'three', 'four'],
                   'b': ['x', 'y', 'x', 'y', 'x', 'x', 'x'],
                  'c': np.random.randn(7)})

print(df2)
print(df2.duplicated('a'))

xxx = df2['c']
print(xxx)

xxx = xxx.where(~df2.duplicated('a',keep='first'), np.nan)
print(xxx)


sss = pd.Series(np.array([1,1,2,2,2,3,3,4,4,5,6,7,8,8,9,9,10,1,1,2,2,3,3]))
print(sss)
roll = sss.rolling(window=2).mean()
print(roll)
print(sss==roll)
print(sss[~(sss==roll)])

print('20191025171049.info'.split('.'))