import pandas as pd
import numpy as np
from io import StringIO,BytesIO

ser = pd.Series(np.random.randn(8))
s=ser


#窗口函数
r = s.rolling(window=60)
'''
count()	Number of non-null observations
sum()	Sum of values
mean()	Mean of values
median()	Arithmetic median of values
min()	Minimum
max()	Maximum
std()	Bessel-corrected sample standard deviation
var()	Unbiased variance
skew()	Sample skewness (3rd moment)
kurt()	Sample kurtosis (4th moment)
quantile()	Sample quantile (value at %)
apply()	Generic apply
cov()	Unbiased covariance (binary)
corr()	Correlation (binary)
r.<TAB>                                          # noqa: E225, E999
r.agg         r.apply       r.count       r.exclusions  r.max         r.median      r.name        r.skew        r.sum
r.aggregate   r.corr        r.cov         r.kurt        r.mean        r.min         r.quantile    r.std         r.var
'''


data =(
               '''height      weight  gender
2000-01-01  42.849980  157.500553    male
2000-01-02  49.607315  177.340407    male
2000-01-03  56.293531  171.524640    male
2000-01-04  48.421077  144.251986  female
2000-01-05  46.556882  152.526206    male
2000-01-06  68.448851  168.272968  female
2000-01-07  70.757698  136.431469    male
2000-01-08  58.909500  176.499753  female
2000-01-09  76.435631  174.094104  female
2000-01-10  45.306120  177.540920    male'''
)

df = pd.read_csv(StringIO(data),sep='\s+')
grouped=gb = df.groupby('gender')
print(gb.count())
'''
gb.agg        gb.boxplot    gb.cummin     gb.describe   gb.filter     gb.get_group  gb.height     gb.last       gb.median     gb.ngroups    gb.plot       gb.rank       gb.std        gb.transform
gb.aggregate  gb.count      gb.cumprod    gb.dtype      gb.first      gb.groups     gb.hist       gb.max        gb.min        gb.nth        gb.prod       gb.resample   gb.sum        gb.var
gb.apply      gb.cummax     gb.cumsum     gb.fillna     gb.gender     gb.head       gb.indices    gb.mean       gb.name       gb.ohlc       gb.quantile   gb.size       gb.tail       gb.weight
'''
df.groupby([pd.Grouper(level='second'), 'A']).sum()
df.groupby(['second', 'A']).sum()

for name, group in df.groupby(['A', 'B']):
    print(name)
    print(group)

grouped.get_group('bar')

grouped = df.groupby(['A', 'B'], as_index=False).aggregate(np.sum)
df.groupby(['A', 'B']).sum().reset_index()
df.groupby(['A', 'B']).describe()
grouped.agg([np.sum, np.mean, np.std])
grouped['C'].agg([lambda x: x.max() - x.min(),lambda x: x.median() - x.mean()])

df.groupby("kind").agg(
    min_height = pd.NamedAgg(column='height', aggfunc='min'),
    max_height = pd.NamedAgg(column='height', aggfunc='max'),
   average_weight = pd.NamedAgg(column='weight', aggfunc=np.mean)
)

df.groupby("kind").agg(
     min_height=('height', 'min'),
    max_height=('height', 'max'),
    average_weight=('weight', np.mean),
 )


df.groupby("kind").height.agg(
     min_height='min',
     max_height='max',
)

grouped.agg({'C': np.sum,
             'D': lambda x: np.std(x, ddof=1)})
grouped.agg({'C': 'sum', 'D': 'std'})


df.groupby('A').rolling(4).B.mean()
df.groupby(df["D"]%4).expanding().sum()

df_re = pd.DataFrame({'date': pd.date_range(start='2016-01-01', periods=4,
                                           freq='W'),
                     'group': [1, 1, 2, 2],
                    'val': [5, 6, 7, 8]}).set_index('date')
df_re.groupby('group').resample('1D').ffill()


dff = pd.DataFrame({'A': np.arange(8), 'B': list('aabbbbcc')})
dff['C'] = np.arange(8)
print(dff.groupby('B').filter(lambda x: len(x) > 2))
print(dff.groupby('B').filter(lambda x: len(x['C']) > 2))
print(dff.groupby('B').head(1))
print(dff.groupby('B').agg(lambda x: x.std()))





