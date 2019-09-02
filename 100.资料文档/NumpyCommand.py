import numpy as np

x = np.empty([3,2], dtype = int)
x = np.zeros(5)
y = np.zeros((5,), dtype = np.int)
z = np.zeros((2,2), dtype = [('x', 'i4'), ('y', 'i4')])
x = np.ones(5)
x = np.ones([2, 2], dtype=int)
s =  b'Hello World'
a = np.frombuffer(s, dtype =  'S1')
x = np.arange(5)
x = np.arange(10,20,2)
a = np.linspace(1,10,11)
a = np.logspace(1.0,  2.0, num =  10)
a = np.logspace(0,9,10,base=2)
a = np.arange(10)
s = slice(2,7,2)   # 从索引 2 开始到索引 7 停止，间隔为2
x = np.array([[1,  2],  [3,  4],  [5,  6]])
y = x[[0,1,2],  [0,1,0]]
x = np.array([[  0,  1,  2],[  3,  4,  5],[  6,  7,  8],[  9,  10,  11]])
rows = np.array([[0,0],[3,3]])
cols = np.array([[0,2],[0,2]])
y = x[rows,cols]
x = np.array([[ 0,  1,  2],[  3,  4,  5],[  6,  7,  8],[  9,  10,  11]])
print (x[x >  5])

a = np.array([np.nan,  1,2,np.nan,3,4,5])
print (a[~np.isnan(a)])

a = np.array([1,  2+6j,  5,  3.5+5j])
print (a[np.iscomplex(a)])

a = np.arange(8)
b = a.reshape(4, 2)

np.transpose(a)
a.T
#numpy.swapaxes
#numpy.concatenate((a1, a2, ...), axis)
np.stack((a,b),1)
np.hstack((a,b))
np.vstack((a,b))
np.split(a,3)
np.split(a,[4,7])

a = np.array([[1,2,3],[4,5,6]])
b = np.resize(a,(3,3))

np.array([[1,2,3],[4,5,6]])
np.append(a, [7,8,9])
np.append(a, [7,8,9])
(np.append(a, [[5,5,5],[7,8,9]],axis = 1))


np.array([[1,2],[3,4],[5,6]])
(np.insert(a,3,[11,12]))
(np.insert(a,1,[11],axis = 0))
(np.insert(a,1,11,axis = 1))

print ('未传递 Axis 参数。 在插入之前输入数组会被展开。')
print (np.delete(a,5))
print ('删除第二列：')
print (np.delete(a,1,axis = 1))
print ('包含从数组中删除的替代值的切片：')
a = np.array([1,2,3,4,5,6,7,8,9,10])
print (np.delete(a, np.s_[::2]))


a = np.array([5,2,6,2,7,5,6,8,2,9])
print ('第一个数组的去重值：')
u = np.unique(a)
print ('去重数组的索引数组：')
u,indices = np.unique(a, return_index = True)
print (indices)
print ('去重数组的下标：')
u,indices = np.unique(a,return_inverse = True)
print (u)
print ('使用下标重构原数组：')
print (u[indices])
print ('返回去重元素的重复数量：')
u,indices = np.unique(a,return_counts = True)

np.bitwise_and(13, 17)
np.bitwise_or(13, 17)
np.invert(np.array([13], dtype = np.uint8))
np.left_shift(10,2)
np.right_shift(40,2)

bin(a)
np.binary_repr(10, width = 8)

print (np.char.add(['hello'],[' xyz']))
print (np.char.add(['hello', 'hi'],[' abc', ' xyz']))

(np.char.multiply('Runoob ',3))
# str: 字符串，width: 长度，fillchar: 填充字符
print (np.char.center('Runoob', 20,fillchar = '*'))
#*******Runoob*******
(np.char.capitalize('runoob'))
(np.char.title('i like runoob'))
(np.char.lower('RUNOOB'))
(np.char.upper('runoob'))
(np.char.split ('i like runoob?'))
(np.char.split ('www.runoob.com', sep = '.'))
(np.char.splitlines('i\rlike runoob?'))
print (np.char.strip('ashok arunooba','a'))
print (np.char.join(':','runoob'))
(np.char.join([':', '-'], ['runoob', 'google']))
(np.char.replace ('i like runoob', 'oo', 'cc'))
a = np.char.encode('runoob', 'cp500')
print (np.char.decode(a,'cp500'))
(np.sin(a*np.pi/180))
#arcsin，arccos，和 arctan 函数返回给定角度的 sin，cos 和 tan 的反三角函数。
#(np.degrees(inv))
print (np.around(a, decimals =  1))
print (np.floor(a))
print (np.ceil(a))
#NumPy 算术函数包含简单的加减乘除: add()，subtract()，multiply() 和 divide()。
#numpy.reciprocal() 函数返回参数逐元素的倒数。如 1/4 倒数为 4/1。
print (np.power(a,2))
print (np.power(a,b))
print (np.mod(a,b))
print (np.remainder(a,b))
print (np.amax(a))
print (np.amax(a, axis =  0))
print (np.ptp(a))
print (np.ptp(a, axis =  1))
(np.percentile(a, 50))
(np.percentile(a, 50, axis=0))
(np.median(a))
(np.median(a, axis =  0))
(np.mean(a))
(np.mean(a, axis =  0))
wts = np.array([4,3,2,1])
print ('再次调用 average() 函数：')
print (np.average(a,weights = wts))
np.std([1,2,3,4])
(np.var([1,2,3,4]))
print (np.sort(a))
print (np.sort(a, axis =  0))
y = np.argsort(x)
numpy.argmax()
numpy.argmin()

#numpy.nonzero() 函数返回输入数组中非零元素的索引。
y = np.where(x >  3)
print (x[y])
condition = np.mod(x,2)  ==  0
print (np.extract(condition, x))
#numpy.ndarray.byteswap() 函数将 ndarray 中每个元素中的字节进行大小端转换。

arr = np.arange(12)
print ('我们的数组：')
print (arr)
print ('创建切片：')
a=arr[3:]
b=arr[3:]
a[1]=123
b[2]=234
print(arr)
#print(id(a),id(b),id(arr[3:]))
#输出结果为：
#我们的数组：
#[ 0  1  2  3  4  5  6  7  8  9 10 11]
#创建切片：
#[  0   1   2   3 123 234   6   7   8   9  10  11]
#4545878416 4545878496 4545878576
b = a.copy()

print(np.dot(a,b))
# vdot 将数组展开计算内积
print (np.vdot(a,b))

print (np.inner(a,b))
#numpy.linalg.solve()
np.savez("runoob.npz", a, b, sin_array = a)
r = np.load("runoob.npz")


























