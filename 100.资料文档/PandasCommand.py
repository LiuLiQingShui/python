import pandas as pd
import numpy as np
from io import StringIO,BytesIO



data = ('a,b,c,d\n'
       '1,2,3,4\n'
        '5,6,7,8\n'
      '9,10,11')

#dtype:                    object,{'b': object, 'c': np.float64, 'd': 'Int64'}
#header:         0,        None,1,2,[0, 1, 2, 3]
#index_col:      0,        False
#sep:                      '|',
#names:                    ['foo', 'bar', 'baz']   #修改colums名称
#usecols:                  ['b', 'd'],[0, 2, 3],lambda x: x.upper() in ['A', 'C'],lambda x: x not in ['a', 'c']   #只读取文件中某些列
#comment:                  '#',   #去掉注释
#skiprows                   4,         #Line numbers to skip (0-indexed) or number of lines to skip (int) at the start of the file.
#parse_dates:               True,[0,1],['a'],[[1, 2], [1, 3]],{'nominal': [1, 2], 'actual': [1, 3]}
df = pd.read_csv(StringIO(data),
                 skiprows=4,
                 header=None,
                 index_col=[0, 1],
                 usecols=['b', 'd'],
                 dtype=object,
                 sep='|',
                 names=['foo', 'bar', 'baz'],
                 comment='#',
                 skip_blank_lines=False,
                 encoding='utf-8',
                 parse_dates=[[1, 2], [1, 3]],
                 date_parser=lambda col: pd.to_datetime(col, utc=True),
                 keep_date_col=True,
                 dayfirst=True,
                 thousands=',',
                 true_values=['Yes'],
                 false_values=['No'],
                 error_bad_lines=False,
                 skipinitialspace=True,
                 )
'''

'''
df.to_csv(path_or_buf="test.csv",
          header=True,
          index=True,
          columns=[0, 1],
          encoding='utf_8_sig',
          sep=', ',
          na_rep='',
          compression='infer',
          date_format='%Y %m %d %H:%M:%S',
          )




data = ('a,b,c,d\n'
 '林腾飞,2,3,4\n'
 '5,6,7,8\n'
'9,10,11')
df = pd.read_csv(StringIO(data), dtype={'b': object, 'c': np.float64, 'd': 'Int64'})
df['date'] = pd.Timestamp('20130101')
df['ints'] = list(range(3))
df['bools'] = True
df.index = pd.date_range('20130101', periods=3)
df = df.sort_index(1, ascending=False)
print(df)
'''
date_format: "iso",'epoch'
date_unit: 'us','s'
'''
df.to_json('jsoncase.json',orient='records',lines=True,force_ascii=False,date_format='iso', date_unit='us',default_handler=str)
df = pd.read_json('jsoncase.json',orient='records',lines=True,dtype={'d': 'float32', 'bools': 'int8'})


#pandas provides a utility function to take a dict or list of dicts and normalize this semi-structured data into a flat table.
from pandas.io.json import json_normalize
data = [{'id': 1, 'name': {'first': 'Coleen', 'last': 'Volk'}},
      {'name': {'given': 'Mose', 'family': 'Regner'}},
       {'id': 2, 'name': 'Faye Raker'}]
json_normalize(data)
data = [{'state': 'Florida',
  'shortname': 'FL',
        'info': {'governor': 'Rick Scott'},
       'counties': [{'name': 'Dade', 'population': 12345},
                   {'name': 'Broward', 'population': 40000},
                    {'name': 'Palm Beach', 'population': 60000}]},
     {'state': 'Ohio',
       'shortname': 'OH',
      'info': {'governor': 'John Kasich'},
      'counties': [{'name': 'Summit', 'population': 1234},
                   {'name': 'Cuyahoga', 'population': 1337}]}]
json_normalize(data, 'counties', ['state', 'shortname', ['info', 'governor']])

data = [{'CreatedBy': {'Name': 'User001'},
         'Lookup': {'TextField': 'Some text',
                    'UserField': {'Id': 'ID001',
                                  'Name': 'Name001'}},
          'Image': {'a': 'b'}
        }]
json_normalize(data, max_level=1)




dates = pd.date_range('1/1/2000', periods=8)
df = pd.DataFrame(np.random.randn(8, 4),
                index=dates, columns=['A', 'B', 'C', 'D'])
print(df.iloc[2,2])
print(type(df.iloc[2,2]))
print(df.iat[2,2])
print(type(df.iat[2,2]))
#直接选择
df['A']
df[['A', 'B']]
df[['B', 'A']] = df[['A', 'B']]
df[0:1]
df[::-1]
#通过laber选择
df.loc[['a', 'b', 'd'], :]
df.loc['20130102':'20130104']
df.loc['d':, 'A':'C']
df.loc['d':, 'A':'C']
df.loc[:, 'C'] = df.loc[:, 'A']#enlargement
df.loc[3] = 5#enlargement
#通过位置选择
df.iloc[1:5, 2:4]
df.iloc[[1, 3, 5], [1, 3]]
df.iloc[1:3, :]
df.iloc[:, 1:3]
df.iloc[1] = {'x': 9, 'y': 99}
#bool选择
df[df['A'] > 0]
criterion = df['a'].map(lambda x: x.startswith('t'))
df[criterion]
df[[x.startswith('t') for x in df['a']]]
df[criterion & (df['b'] == 'x')]
df.loc[criterion & (df['b'] == 'x'), 'b':'c']
s_mi = pd.Series(np.arange(6),index=pd.MultiIndex.from_product([[0, 1], ['a', 'b', 'c']]))
s_mi.iloc[s_mi.index.isin([(1, 'a'), (2, 'b'), (0, 'c')])]
s_mi.iloc[s_mi.index.isin(['a', 'c', 'e'], level=1)]
df = pd.DataFrame({'vals': [1, 2, 3, 4], 'ids': ['a', 'b', 'f', 'n'],  'ids2': ['a', 'n', 'c', 'n']})
values = ['a', 'b', 1, 3]
df.isin(values)
values = {'ids': ['a', 'b'], 'ids2': ['a', 'c'], 'vals': [1, 3]}
row_mask = df.isin(values).all(1)
df.where(df < 0, -df, inplace=True)
df[df < 0]
df[df < 0] = 0
df[df[1:4] > 0] = 3
df.where(df > 0, df['A'], axis='index')
df.apply(lambda x, y: x.where(x > 0, y), y=df['A'])
#去除重复项
df.duplicated('a', keep=False)
df.drop_duplicates('a', keep=False)
df.duplicated(['a', 'b'])
df.drop_duplicates(['a', 'b'])
df[~df.index.duplicated(keep='last')]
#选择出特定的数据
df.lookup(list(range(0, 10, 2)), ['B', 'C', 'A', 'B', 'D'])
# array([0.3506, 0.4779, 0.4825, 0.9197, 0.5019])
df.set_index(['a', 'b'], inplace=True,append=True,drop=False)
index = pd.Index([1, np.nan, 3, 4])
df.index = index




#多重标签，引用
arrays = [['bar', 'bar', 'baz', 'baz', 'foo', 'foo', 'qux', 'qux'],
        ['one', 'two', 'one', 'two', 'one', 'two', 'one', 'two']]
s = pd.Series(np.random.randn(8), index=arrays)
print(s)
iterables = [['bar', 'baz', 'foo', 'qux'], ['one', 'two']]
pd.MultiIndex.from_product(iterables, names=['first', 'second'])
df = pd.DataFrame([['bar', 'one'], ['bar', 'two'],
                 ['foo', 'one'], ['foo', 'two']],
                 columns=['first', 'second'])
df = pd.DataFrame([['bar', 'one'], ['bar', 'two'],
                   ['foo', 'one'], ['foo', 'two']],
                 columns=['first', 'second'])
pd.MultiIndex.from_frame(df)
index=[]
index.get_level_values(0)
index.get_level_values('second')
df['bar', 'one']
df['bar']['one']
df.loc[('bar', 'two')]
df.loc[('bar', 'two'), 'A']
df.loc['ar']
df.loc['baz':'foo']
df.loc[('baz', 'two'):('qux', 'one')]
df.loc[('baz', 'two'):'foo']
df.loc[[('bar', 'two'), ('qux', 'one')]]
s.loc[[("A", "c"), ("B", "d")]]
s.loc[(["A", "B"], ["c", "d"])]
df.loc[(slice('A1', 'A3'), slice(None), ['C1', 'C3']), :]
idx = pd.IndexSlice
df.loc[idx[:, :, ['C1', 'C3']], idx[:, 'foo']]
df.loc[idx[:, :, ['C1', 'C3']], :] = df * 1000
midx = pd.MultiIndex(levels=[['zero', 'one'], ['x', 'y']],
                  codes=[[1, 1, 0, 0], [1, 0, 1, 0]])
print(midx)
df = pd.DataFrame(np.random.randn(4, 2), index=midx)
print(df)
df2 = df.mean(level=0)
print(df2)
midx = pd.MultiIndex(levels=[['zero', 'one'], ['x', 'y']],
                  codes=[[1, 1, 0, 0], [1, 0, 1, 0]])
print(midx)
df = pd.DataFrame(np.random.randn(4, 2), index=midx)
print(df)
df2 = df.mean(level=0)
print(df2)
df2.reindex(df.index, level=0)
df_aligned, df2_aligned = df.align(df2, level=0)
df[:5].reorder_levels([1, 0], axis=0)
df.rename(columns={0: "col0", 1: "col1"})
df.rename(index={"one": "two", "y": "z"})
df.sort_index()
df.sort_index(level=1)
df.T.sort_index(level=1, axis=1)




#合并
df = pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'],
                    'B': ['B8', 'B9', 'B10', 'B11'],
                    'C': ['C8', 'C9', 'C10', 'C11'],
                   'D': ['D8', 'D9', 'D10', 'D11']},
                   index=[8, 9, 10, 11])


frames = [df, df, df]
frames = [ frames for item in [0,1,32] ]
pd.concat(frames,
          axis=1,
          join='inner',
          ignore_index=True,
          keys=['x', 'y', 'z'],#只保留这些索引
          levels=None,
          names=None,
          verify_integrity=False,
          copy=True)


left = pd.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'],
                     'key2': ['K0', 'K1', 'K0', 'K1'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                    'B': ['B0', 'B1', 'B2', 'B3']})
right = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                    'key2': ['K0', 'K0', 'K0', 'K0'],
                     'C': ['C0', 'C1', 'C2', 'C3'],
                   'D': ['D0', 'D1', 'D2', 'D3']})
'''
how:    left,right,outer,inner
validate: one_to_one,one_to_many,many_to_many,many_to_one
'''
result = pd.merge(left,
                  right,
                  on=['key1', 'key2'],
                  how='inner',
                  validate="one_to_many",
                  indicator=True,
                  sort=False,
                  suffixes=['_l', '_r'])
pd.merge(left, right, left_on='key', right_index=True, how='outer')
result = pd.merge(left.reset_index(), right.reset_index(), on=['key'], how='inner').set_index(['key','Y'])
df1=df
df2=df
result = df1.combine_first(df2) #覆盖数据。用于更新场景
df1.update(df2) #覆盖数据
left.join(right, on=['abc', 'xy'], how='inner')


#数据透视表
df=[]
df.pivot(index='date', columns='variable', values='value')
#aggfunc: function to use for aggregation, defaulting to numpy.mean.
# aggfunc:  'mean' ,np.sum,'size',['mean', 'sum']
pd.pivot_table(df, values='D', index=['B'], columns=['A', 'C'], aggfunc=np.sum,margins=True, fill_value=0)
pd.to_string(na_rep='')
#level: ['animal', 'hair_length'],[1, 2]
df.stack(level=['animal', 'hair_length'])
df.stack(level=[1, 2])
df.stack('exp')
df.unstack(0)
pd.crosstab(df.A, df.B, values=df.C, aggfunc=np.sum, normalize=True,  margins=True)
ages = np.array([10, 15, 13, 12, 23, 25, 28, 59, 60])
c = pd.cut(ages, bins=[0, 18, 35, 70])
pd.get_dummies(pd.cut(ages, bins=[0, 18, 35, 70]))
#prefix: 'new_prefix',['from_A', 'from_B']
pd.get_dummies(df, columns=['A','B'], prefix='new_prefix')
labels, uniques = pd.factorize(df['a'])
cols = np.array(['key', 'row', 'item', 'col'])
df = cols + pd.DataFrame((np.random.randint(5, size=(20, 4))// [2, 1, 2, 1]).astype(str))
df.explode('values')
df.assign(var1=df.var1.str.split(',')).explode('var1')



#字符串操作
s2 = pd.Series(['a_b_c', 'c_d_e', np.nan, 'f_g_h'])
s2.str.split('_')
s2.str.split('_').str.get(1)
s2.str.split('_').str[1]
s2.str.split('_', expand=True, n=1)
s2.str.replace(r'-\$', '-')
s2.str.replace('-$', '-', regex=False)
pat = r'[a-z]+'
def repl(m):
    return m.group(0)[::-1]
pd.Series(['foo 123', 'bar baz', np.nan]).str.replace(pat, repl)

pat = r"(?P<one>\w+) (?P<two>\w+) (?P<three>\w+)"
def repl(m):
    return m.group('two').swapcase()
pd.Series(['Foo Bar Baz', np.nan]).str.replace(pat, repl)
s2.str.cat(sep=',', na_rep='-')
t2= s2
s2.str.cat(t2, na_rep='-')
s2.str.cat([t2, t2.to_numpy()], join='left')
s2.str[0]
s2.index.str.extract("(?P<letter>[a-zA-Z])", expand=False)
two_groups = '(?P<letter>[a-z])(?P<digit>[0-9])'
pd.Series(["a1a2", "b1", "c1"]).str.extractall(two_groups)
pd.Series(['1', '2', '3a', '3b', '03c']).str.contains(two_groups,na=False)
pd.Series(['1', '2', '3a', '3b', '03c']).str.match(two_groups)
'''
Method summary
Method	Description
cat()	Concatenate strings
split()	Split strings on delimiter
rsplit()	Split strings on delimiter working from the end of the string
get()	Index into each element (retrieve i-th element)
join()	Join strings in each element of the Series with passed separator
get_dummies()	Split strings on the delimiter returning DataFrame of dummy variables
contains()	Return boolean array if each string contains pattern/regex
replace()	Replace occurrences of pattern/regex/string with some other string or the return value of a callable given the occurrence
repeat()	Duplicate values (s.str.repeat(3) equivalent to x * 3)
pad()	Add whitespace to left, right, or both sides of strings
center()	Equivalent to str.center
ljust()	Equivalent to str.ljust
rjust()	Equivalent to str.rjust
zfill()	Equivalent to str.zfill
wrap()	Split long strings into lines with length less than a given width
slice()	Slice each string in the Series
slice_replace()	Replace slice in each string with passed value
count()	Count occurrences of pattern
startswith()	Equivalent to str.startswith(pat) for each element
endswith()	Equivalent to str.endswith(pat) for each element
findall()	Compute list of all occurrences of pattern/regex for each string
match()	Call re.match on each element, returning matched groups as list
extract()	Call re.search on each element, returning DataFrame with one row for each element and one column for each regex capture group
extractall()	Call re.findall on each element, returning DataFrame with one row for each match and one column for each regex capture group
len()	Compute string lengths
strip()	Equivalent to str.strip
rstrip()	Equivalent to str.rstrip
lstrip()	Equivalent to str.lstrip
partition()	Equivalent to str.partition
rpartition()	Equivalent to str.rpartition
lower()	Equivalent to str.lower
casefold()	Equivalent to str.casefold
upper()	Equivalent to str.upper
find()	Equivalent to str.find
rfind()	Equivalent to str.rfind
index()	Equivalent to str.index
rindex()	Equivalent to str.rindex
capitalize()	Equivalent to str.capitalize
swapcase()	Equivalent to str.swapcase
normalize()	Return Unicode normal form. Equivalent to unicodedata.normalize
translate()	Equivalent to str.translate
isalnum()	Equivalent to str.isalnum
isalpha()	Equivalent to str.isalpha
isdigit()	Equivalent to str.isdigit
isspace()	Equivalent to str.isspace
islower()	Equivalent to str.islower
isupper()	Equivalent to str.isupper
istitle()	Equivalent to str.istitle
isnumeric()	Equivalent to str.isnumeric
isdecimal()	Equivalent to str.isdecimal
'''




#处理Na数据
#Note If you want to consider inf and -inf to be “NA” in computations, you can set pandas.options.mode.use_inf_as_na = True.
df=pd.DataFrame([1,2,3])
df.isna()
df.notna()
s = pd.Series(["a", "b", "c"])
s.loc[1] = np.nan
df.fillna(0)
df['one'].fillna('missing')
df.fillna(method='pad')
df.fillna(method='pad', limit=1)
#ffill() 、fillna(method='ffill')
dff=df
dff.fillna(dff.mean())
dff.fillna(dff.mean()['B':'C'])
dff.where(pd.notna(dff), dff.mean(), axis='columns')
df.dropna(axis=0)
df['one'].dropna()

df.interpolate().plot()
#For a floating-point index, use method='values': for time index, use method='time'
#methon: 'linear', 'quadratic', 'cubic,'barycentric,method='akima'

df.interpolate(method='time')
df.interpolate(method='values')
df.interpolate(method='pchip')
df.interpolate(method='spline', order=2)
df.interpolate(method='polynomial', order=2)
ser = pd.Series(np.sort(np.random.uniform(size=100)))
new_index = ser.index | pd.Index([49.25, 49.5, 49.75, 50.25, 50.5, 50.75])
interp_s = ser.reindex(new_index).interpolate(method='pchip')
interp_s[49:51]
ser.interpolate(limit=1, limit_direction='both')
ser.interpolate(limit_direction='both')

ser.replace([0, 1, 2, 3, 4], [4, 3, 2, 1, 0])
ser.replace({0: 10, 1: 100})
ser.replace([1, 2, 3], method='pad')
df.replace(['a', '.'], ['b', np.nan], inplace=True)
df.replace([r'\.', r'(a)'], ['dot', r'\1stuff'], regex=True)
df.replace({'b': '.'}, {'b': np.nan})
df.replace({'b': r'\s*\.\s*'}, {'b': np.nan}, regex=True)
df.replace({'b': {'b': r''}}, regex=True)
df.replace(regex={'b': {r'\s*\.\s*': np.nan}})
df.replace({'b': r'\s*(\.)\s*'}, {'b': r'\1ty'}, regex=True)
df.replace([r'\s*\.\s*', r'a|b'], np.nan, regex=True)





#分类类型
s = pd.Series(["a", "b", "c", "a"], dtype="category")

df = pd.DataFrame({"A": ["a", "b", "c", "a"]})
df["B"] = df["A"].astype('category')

raw_cat = pd.Categorical(["a", "b", "c", "a"], categories=["b", "c", "d"],ordered=False)

df = pd.DataFrame({'A': list('abca'), 'B': list('bccd')}, dtype="category")

df_cat = df.astype('category')

from pandas.api.types import CategoricalDtype
s = pd.Series(["a", "b", "c", "a"])
cat_type = CategoricalDtype(categories=["b", "c", "d"],ordered=True)
s_cat = s.astype(cat_type)
df = pd.DataFrame({'A': list('abca'), 'B': list('bccd')})
cat_type = CategoricalDtype(categories=list('abcd'),ordered=True)
df_cat = df.astype(cat_type)
splitter = np.random.choice([0, 1], 5, p=[0.5, 0.5])
s = pd.Series(pd.Categorical.from_codes(splitter, categories=["train", "test"]))

CategoricalDtype(['a', 'b', 'c'])
CategoricalDtype(categories=['a', 'b', 'c'], ordered=None)
CategoricalDtype(['a', 'b', 'c'], ordered=True)
CategoricalDtype(categories=['a', 'b', 'c'], ordered=True)
CategoricalDtype()
CategoricalDtype(categories=None, ordered=None)
df.describe()

s.cat.set_categories(["one", "two", "three", "four"])
s.cat.rename_categories([1, 2, 3])
s = s.cat.add_categories([4])
s = s.cat.remove_categories([4])
s.cat.remove_unused_categories()

s = s.cat.set_categories([2, 3, 1], ordered=True)
s.sort_values(inplace=True)

dfs = pd.DataFrame({'A': pd.Categorical(list('bbeebbaa'),
                                      categories=['e', 'a', 'b'],
                                       ordered=True),
                   'B': [1, 2, 1, 2, 2, 1, 2, 1]})
dfs.sort_values(by=['A', 'B'])

df.apply(lambda col: col.dtype, axis=0)




#强制转换成数字，非数字会转换成NaN
df['col_1'] = pd.to_numeric(df['col_1'], errors='coerce')
#查看某一列的类型统计
df['col_1'].apply(type).value_counts()