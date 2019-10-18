import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pymongo
import base64
import time
import pytz

print(1)
print('a')
print(str('a'))


df_base = np.array([[1,np.nan,1],[1,1,np.nan]])
print(df_base)
df_base[np.isnan(df_base)]=-1
print(df_base)