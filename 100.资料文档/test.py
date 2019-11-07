import pandas as pd
import numpy as np
from io import StringIO,BytesIO
import time
import datetime


import pytz


import matplotlib.pyplot as plt

from pandas.api.types import CategoricalDtype



s = pd.qcut(range(5), 4)
print(type(s))
print(s)
print(s[1])
s = pd.qcut(range(5), 3, labels=["good", "medium", "bad"])
print(s)
print(s[1])
s = pd.qcut(range(5), 4, labels=False)
print(s)
print(s[1])





s = pd.Series([1,2,3,4,5,6,7,8,9,10])
bins = pd.IntervalIndex.from_tuples([(1,2),(3,4),(8,9)], closed='both')
StaticStageCategories = pd.cut(s, bins,
                               labels=['stage 1', 'stage 2', 'stage 3','stage 1', 'stage 2', 'stage 3','stage 1', 'stage 2', 'stage 3','stage 1'])
print(StaticStageCategories)