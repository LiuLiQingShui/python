import pandas as pd
import numpy as np
from io import StringIO,BytesIO
import time


tsdf = pd.DataFrame(np.random.randn(1000, 3),
                  index=pd.date_range('1/1/2000', periods=1000),
                   columns=['A', 'B', 'C'])
print(tsdf)


tsdf['D']=[1]*250+[2]*250+[3]*250+[4]*250
#tsdf.iloc[::2] = np.nan
print(tsdf)
grouped = tsdf.groupby(tsdf["D"]%4)
print(grouped.describe())
print(grouped.sum())

print(grouped.agg({'C': np.sum,
            }))
print(grouped.agg({ 'D': np.min}))

print(grouped.agg(
     min_height=('C', np.sum),
    max_height=('D', 'max'),
 ))

