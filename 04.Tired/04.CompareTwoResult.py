import os
import numpy as np
import pandas as pd

# pd.set_option('expand_frame_repr',False)
# result_1 = pd.read_csv(r'F:\01Cplusplus\01.Tired\From fenyang\sub3\Result\1\Result\Result_details.csv',encoding='utf_8_sig',usecols=['Alarm','DMS result','Video Name','Mode','result'])
# result_2 = pd.read_csv(r'F:\01Cplusplus\01.Tired\From fenyang\sub3\Result\2\Result\Result_details.csv',encoding='utf_8_sig',usecols=['Alarm','DMS result','Video Name','Mode','result'])
#
# ResultCompare = pd.merge(result_1,result_2,how='outer',on=['Alarm','DMS result','Video Name','Mode'],suffixes=('_1','_2'))
# ResultCompare.to_csv('ResultCompare.csv',encoding='utf_8_sig',index=False)


df_compare = pd.read_csv(r'ResultCompare.csv',encoding='utf_8_sig')
df_compare = df_compare[df_compare['result_1']!=df_compare['result_2']]
print(df_compare)