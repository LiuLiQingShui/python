


#list
list.append(x)
list.extend(iterable)
list.insert(i,x)
list.pop([i])
list.clear()
list.index(x[,start[,end]])
list.remove(x)
list.count(x)
list.sort(key =None,reverse=False)
list.reverse()
list.copy()

from collections import deque
queue = deque(["Eric", "John", "Michael"])
queue.append("Terry")           # Terry arrives
queue.append("Graham")          # Graham arrives
queue.popleft()                 # The first to arrive now leaves
'Eric'
queue.popleft()                 # The second to arrive now leaves
'John'
queue                           # Remaining queue in order of arrival
deque(['Michael', 'Terry', 'Graham'])

squares = list(map(lambda x: x**2, range(10)))
squares = [x**2 for x in range(10)]
[(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
vec = [[1,2,3], [4,5,6], [7,8,9]]
[num for elem in vec for num in elem]

from math import pi
[str(round(pi, i)) for i in range(1, 6)]

matrix = [
     [1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12],
 ]
[[row[i] for row in matrix] for i in range(4)]
list(zip(*matrix))
a = [-1, 1, 66.25, 333, 333, 1234.5]
del a[0]
del a[2:4]
del a[:]
del a #a不存在了

#tuple
t = 12345, 54321, 'hello!'
singleton = 'hello',
x, y, z = t

#sets
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
basket = set(['apple', 'orange', 'apple', 'pear', 'orange', 'banana'])
'orange' in basket
'crabgrass' in basket
a = set('abracadabra')
b = set('alacazam')
a - b
a | b
a & b
a ^ b
{x for x in 'abracadabra' if x not in 'abc'}

#dict
tel = {'jack': 4098, 'sape': 4139}
del tel['sape']
list(tel)
sorted(tel)
'guido' in tel
print(dict([('sape', 4139), ('guido', 4127), ('jack', 4098)]))
print(dict((('sape', 4139), ('guido', 4127), ('jack', 4098))))
print(dict((['sape', 4139], ['guido', 4127], ['jack', 4098])))
dict(sape=4139, guido=4127, jack=4098)
{x: x**2 for x in (2, 4, 6)}


#looping techniques
knights = {'gallahad': 'the pure', 'robin': 'the brave'}
for k, v in knights.items():
    print(k, v)
for i, v in enumerate(['tic', 'tac', 'toe']):
    print(i, v)
questions = ['name', 'quest', 'favorite color']
answers = ['lancelot', 'the holy grail', 'blue']
for q, a in zip(questions, answers):
    print('What is your {0}?  It is {1}.'.format(q, a))
for i in reversed(range(1, 10, 2)):
    print(i)
basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
for f in sorted(set(basket)):
    print(f)

#more on conditions
#numerical>comparison>Boolean operators
a,b,c = 1,2,3
print((a < b == c+1) not in [0,5,9] and not c is not b)
(a < c == b+1) not in [0,5,9] and  not c is not b


#conmparing sequences and other types
(1, 2, 3)              < (1, 2, 4)
[1, 2, 3]              < [1, 2, 4]
'ABC' < 'C' < 'Pascal' < 'Python'
(1, 2, 3, 4)           < (1, 2, 4)
(1, 2)                 < (1, 2, -1)
(1, 2, 3)             == (1.0, 2.0, 3.0)
(1, 2, ('aa', 'ab'))   < (1, 2, ('abc', 'a'), 4)


#modules
import fibo
from fibo import fib, fib2
from fibo import * #use carefully
import fibo as fib
from fibo import fib as fibonacci
#if it’s just one module you want to test interactively, use importlib.reload(), e.g.
import importlib
importlib.reload(modulename)

#executing modeles as scripts
#This is often used either to provide a convenient user interface to a module, or for testing purposes (running the module as a script executes a test suite).
if __name__ == "__main__":
    import sys
    fib(int(sys.argv[1]))
import builtins
dir(builtins)

import sound.effects.echo
from sound.effects import echo
from sound.effects.echo import echofilter


#Formatted String Literals
import math
print(f'The value of pi is approximately {math.pi:.3f}.')
print(f'{name:10} ==> {phone:10.1f}')

print('The story of {0}, {1}, and {other}.'.format('Bill', 'Manfred',
                                                       other='Georg'))


print('The story of {}, {}, and {other}.'.format('Bill', 'Manfred',
                                                       other='Georg'))
table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 8637678}
print('Jack: {Jack:d}; Sjoerd: {Sjoerd:d}; Dcab: {Dcab:d}'.format(**table))
'12'.zfill(5) #pads a numeric string on the left with zeros. It understands about plus and minus signs:
picname = '{:0>6d}'.format(i+1)+'.jpg'

f.tell()
f.seek(offset, whence)

#异常处理
def divide(x, y):
    try:
        result = x / y
    except ZeroDivisionError:
        print("division by zero!")
    else:
        print("result is", result)
    finally:
        print("executing finally clause")




'''
You might have noticed that methods like insert, remove or sort that only modify the list have no return value printed – they return the default None. 1 This is a design principle for all mutable data structures in Python
 *-operator to unpack  a list or tuple
**-operator to unpack  a  dictionary or mapping
Note that multiple assignment is really just a combination of tuple packing and sequence unpacking.
'''


#build-in
all(),any()
bin(3),format(14, '#b'), format(14, 'b')
callable(object)
chr(97) ,ord('a')
delattr(object, name),setattr(),getattr(x, 'foobar'),hasattr(object, name)
dir(module)
divmod(a,b)
list(enumerate(seasons.start=1))
[(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]
globals()
hash()
help(int)
isinstance()
issubclass()
map(function, iterable, ...)
zip()

constants defined to be false: None and False.
zero of any numeric type: 0, 0.0, 0j, Decimal(0), Fraction(0, 1)
empty sequences and collections: '', (), [], {}, set(), range(0)

x = {'agbadsfasdf':'1'}
y = {'agbadsfasdf':'1'}
z = x
print(id(x),id(y),id(z))
print(y is x)
print(z is x)
print(y == x)
print(z == x)


<,<=,>,>=,==,!=,is,is not,in ,not in
x | y, x ^ y,x & y,x << n,x >>n,~x,

n = -37
n.bit_length()
n.to_bytes((n.bit_length() + 7) // 8, byteorder='little', signed=True)
print(int.from_bytes([255, 0, 0], byteorder='big'))
print(int.from_bytes(b'\xff\x00\x00', byteorder='big'))

Common Sequence Operations
x in s, x not in s, s + t, s * n or n * s, s[i], s[i:j], s[i:j:k], len(s), min(s), max(s), s.index(x[, i[, j]]), s.count(x)
Mutable Sequence Types
s[i] = x, s[i:j] = t, del s[i:j], s[i:j:k] = t, del s[i:j:k], s.append(x), s.clear(), s.copy(), s.extend(t) or s += t, s *= n, s.insert(i, x), s.pop([i]), s.remove(x),s.reverse()

list(range(0, -10, -1))
str.capitalize(),str.casefold(),str.center(width[, fillchar]),str.count(sub[, start[, end]]),str.encode(encoding="utf-8", errors="strict"),str.find(sub[, start[, end]]),str.zfill(width),

b'still allows embedded "double" quotes'
 
#优先级
'''
Level 1: Boolean Operations
x or y,x and y,not x

Level 2:Comparisons,
x < y <= z
<,<=,>,>=,==,!=,is,is not,in , not in

level 3:Bitwise Operations
x | y, x ^ y, x & y , x<<n, x>>n, ~x

Level 4:
+,-,*,/,//,%,divmod,-x,+x,abs(x),int(x),float(x),complex(re,im),c.conjugate(),divmod(x,y),pow(x,y),x**y
float(nan),float(+inf),float(-inf)
round(x,n),math.floor(x),math.ceil(x)

'''



'''
int.bit_length()
int.to_bytes()
int.from_bytes()
float.as_integer_ratio()
float.is_integer()
'''

'''
x in s, x not in s, s+t,s*n,s[i],s[i:j],s[i:j:k],len(s),min(s),max(s),s.index(x,i,j),s.count(x)
s[i]=x,s[i:j]=t,s[i:j:k]=t,del s[i:j:k],s.append(x),s.clear(),s.copy(),s.extend(t).s+=t,s*=n,s.insert(i,x),s.pop([i]),s.remove(x),s.reverse()
t must have the same length as the slice it is replacing.

List: sort

str:capitalize(),count(sub),encode(),expandtabs(4),find(sub),format(),isalnum(),isalpha(),isdecimal(),isdigit(),isnumeric(),
join(),ljut(width),lstrip(),replace,split(),splitlines(),strip(),title(),

Bytes: count(),decode(),find(),join(),replace(),rfind(),split(),strip(),......
Bytes simlilar with str

Set: len(s),isdisjoint(),issubset(),set<=other,issuperset(), set>=other,union(),set|other|...,intersection(),set&other&...,difference(),
set - other -...,symmetric_diference(other),set^other,
update(*others),set |=other |..., intersection_update(*others),set &= other &,..., difference_update(*other),set-=ohter|...,
symmetric_difference_update(other),set ^=other, add(),remove(),discard(),pop(),clear(),

Dict:clear,copy,get,iter(d),keys(),items(),pop(key),popitem(),update([other]),
'''

'''
Text Processing Services:
'{2}, {1}, {0}'.format('a', 'b', 'c')
coord = {'latitude': '37.24N', 'longitude': '-115.81W'}
>>> 'Coordinates: {latitude}, {longitude}'.format(**coord)
coord = (3, 5)
>>> 'X: {0[0]};  Y: {0[1]}'.format(coord)
'{:<30}'.format('left aligned')
'{:>30}'.format('right aligned')
'{:^30}'.format('centered')
'{:*^30}'.format('centered')  # use '*' as a fill char
'{:+f}; {:+f}'.format(3.14, -3.14)
'{: f}; {: f}'.format(3.14, -3.14)
 '{:-f}; {:-f}'.format(3.14, -3.14)
 "int: {0:d};  hex: {0:x};  oct: {0:o};  bin: {0:b}".format(42)
 "int: {0:d};  hex: {0:#x};  oct: {0:#o};  bin: {0:#b}".format(42)
 '{:,}'.format(1234567890)
 'Correct answers: {:.2%}'.format(points/total)
d = datetime.datetime(2010, 7, 4, 12, 15, 58)
>>> '{:%Y-%m-%d %H:%M:%S}'.format(d)

re:re.compile,re.search.re.match,re.fullmatch,re.split,re.findall,re.finditer,re.sub,
compile.search,compile.match,compile.fullmatch,
match.group(0),match.group(1),match.group('first_name'),
'''


'''
Binary data service:
struck: pack,pack_into,unpack,unpack_from,iter_unpack,

'''

'''
datetime: minyear,maxyear
datetime.date: year,month,day
datetime.time: hour,minute,second,microsecond
datetime.datetime: year,month,day,hour,minute,second,microsecond
datetime.timedelta
datetime.tzinfo
datetime.timezone

timedelta: 
timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
datetime.timedelta(days=64, seconds=29156, microseconds=10)
timedelta.min,max,resolution
+,-*,/,//,%,abs

date:
today(),fromtimestamp(),fromordinal(),fromisoformat('2019-12-04'),fromisocalendar(year, week, day),
min,max,resolution,year,month,day,date2 = date1 + timedelta,replace(year=self.year, month=self.month, day=self.day),isocalendar(),
isoformat(),ctime(),strftime(format)

datetime:
datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0),
today(),now(tz=None),datetime.utcnow(),fromtimestamp(timestamp,tz=None),combine(date,time,tzinfo=self.tzinfo)
datetime.fromisoformat('2011-11-04'),datetime.fromisoformat('2011-11-04T00:05:23'),datetime.fromisoformat('2011-11-04T00:05:23+04:00'),fromisocalendar(year, week, day),strptime(date_string, format)
min,max,resolution,year,month。。。tzinfo,datetime2 = datetime1 + timedelta, date(),time(),timetz(),replace(),
astimezone(tz=None), replace(tzinfo=tz),replace(tzinfo=None)
isoformat(),ctime(),strftime(),

time:
datetime.time(hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0),
time.fromisoformat('04:23:01+04:00')
replace(),isoformat(),strftime(),
'''

'''
ChainMap(adjustments, baseline),
Counter('abracadabra').most_common(3),
deque,
namedtuple('Point', ['x', 'y'])
'''


'''
size = None
if isinstance(myvar, collections.abc.Sized):
    size = len(myvar)
'''

'''
heapq: Heaps are binary trees for which every parent node has a value less than or equal to any of its children. This implementation uses arrays for which heap[k] <= heap[2*k+1] and heap[k] <= heap[2*k+2] 

bisect:
bisect_left(a, x, lo=0, hi=len(a)),bisect_right(a, x, lo=0, hi=len(a)),bisect(a, x, lo=0, hi=len(a))
insort_left(a, x, lo=0, hi=len(a)),insort_right(a, x, lo=0, hi=len(a)),insort(a, x, lo=0, hi=len(a))

copy:  copy,deepcopy

pprint.pprint(project_info, depth=1, width=60)


class Shake(Enum):
...     VANILLA = 7
...     CHOCOLATE = 4
...     COOKIES = 9
...     MINT = 3
Color(1),Color['RED'],member.name,member.value
for name, member in Shape.__members__.items():
...     name, member
'''


'''
math:   ceil,comb(n,k),perm(),copysign(x,y),fabs(x),floor(x),fmod(x,y),frexp(x),fsum(),gcd(a,b),isclose(),isfinite(),isinf(),isnan(),isqrt(),
        isqrt(),modf(x),prod(),exp(),expml,log,loglp,log2,log10,pow(x,y),sqrt(x),
        acos(x),asin(x),atan(x),atan2(y/x),cos,dist(p,q),hypot,sin,tan,degrees,radians,cosh(x),asinh(x),atanh(x),cosh,sinh,tanh
        pi,e,tau,inf,nan,
cmath:

decimal:    Fraction(-8, 5),

random:     randrange(),randint(a,b),choice(seq),shuffle(),sample(),random(),uniform(a,b),

statistics: mean,stdev,variance,
'''

'''
itertools:  count(10),cycle('ABCD'),repeat(10, 3),accumulate([1,2,3,4,5]),chain.from_iterable,

functools:
'''


'''
os.path:

c = ('test.py')
print(os.path.join(c,'d','e','f','g'))
os.path.split(c)
print(os.path.basename(c))
print(os.path.dirname(c))
print(os.path.splitdrive(c))

print(os.path.exists(c))
os.path.lexists(c)
print(os.path.isfile(c))
print(os.path.isdir(c))
print(os.path.isabs(c))
os.path.islink(c)

print(os.path.getsize(c))
print(os.path.getatime(c))
print(os.path.getmtime(c))
os.path.getctime(c)

print(os.path.expanduser('~c'))
print(os.path.expandvars('$JAVA_HOME'))
print(os.path.normcase(c))
os.path.normpath(c)
d = os.path.abspath('test1.py')
print(os.path.realpath(d),'aaaaa')
print(os.path.relpath(d, start=os.curdir))
print(os.path.samefile(c,c))
f1 = 1
f2 = 2
os.path.sameopenfile(f1,f2)
(os.path.supports_unicode_filenames)
os.path.commonprefix(['/usr/lib', '/usr/local/lib'])
'/usr/l'
os.path.commonpath(['/usr/lib', '/usr/local/lib'])
'/usr'

'''

'''
for p,dir,file in os.walk(os.getcwd()):
    print(p,dir,file)
print(os.getcwd())
os.chdir()
os.chmod()
os.listdir()
os.mkdir()
os.remove()
os.rename()
os.rmdir()
os.stat()
os.walk()
print(os.name)
print(os.environ)
print(os.getenv('JAVA_HOME'))
os.access()
'''

'''
filecmp
glob.glob('./[0-9].*')

'''

'''
shutil:  copy,copy2,copytree,rmtree,move,chown,
'''


'''
pickle: dump,dumps,load,loads

sqlite3:
import sqlite3
conn = sqlite3.connect('example.db')
conn:   cursor,commit,rollback,close,execute,executemany,executescript,create_function,interrupt,backup,
c = conn.cursor()
c:  execute,executemany,executescript,fetchone,fetchmany(size=10),fetchall(),close(),lastrowid,arraysize,description,connection
c.execute('CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)')

c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
conn.commit()
conn.close()
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
print(c.fetchone())
con = sqlite3.connect(":memory:")
r = c.fetchone()
>>> type(r)
<class 'sqlite3.Row'>
>>> tuple(r)
('2006-01-05', 'BUY', 'RHAT', 100.0, 35.14)
>>> len(r)
5
>>> r[2]
'RHAT'
>>> r.keys()
['date', 'trans', 'symbol', 'qty', 'price']
>>> r['qty']
100.0
>>> for member in r:
...     print(member)

'''


'''
zlib: compress,compressobj,decompress,decompressobj,
compress:   compress,flush,copy
decompress: decompress,flush,copy

import gzip
with gzip.open('/home/joe/file.txt.gz', 'rb') as f:
    file_content = f.read()
content = b"Lots of content here"
with gzip.open('/home/joe/file.txt.gz', 'wb') as f:
    f.write(content)   
with open('/home/joe/file.txt', 'rb') as f_in:
    with gzip.open('/home/joe/file.txt.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

import bz2
with bz2.open("myfile.bz2", "wb") as f:
    # Write compressed data to file
    unused = f.write(data)
with bz2.open("myfile.bz2", "rb") as f:
    # Decompress data from file
    content = f.read()

zipfile:
with zipfile.ZipFile('spam.zip', 'w') as myzip:
    myzip.write('eggs.txt')
zipfile.ZipFile: namelist(),infolist(),getinfo(name), ZipFile.open(name, mode='r', pwd=None, *, force_zip64=False),extract(),extractall,read(),write,writestr,filename

import tarfile
tar = tarfile.open("sample.tar.gz")
tar.extractall()
tar.close()
def py_files(members):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ".py":
            yield tarinfo
tar = tarfile.open("sample.tar.gz")
tar.extractall(members=py_files(tar))
tar.close()
with tarfile.open("sample.tar", "w") as tar:
    for name in ["foo", "bar", "quux"]:
        tar.add(name)
tar = tarfile.open("sample.tar.gz", "r:gz")
tar = tarfile.open("sample.tar.gz", "w:gz")
'''

'''
csv:
csv: reader,writer
with open('some.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    reader = csv.reader(f, delimiter=':', quoting=csv.QUOTE_NONE)
    for row in reader:
        print(row)
with open('some.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow('aaaaa')
    writer.writerows(someiterable)
    
configparser
class configparser.ConfigParser:    sections(),add_section(section),has_section(section),options(section),has_option(section, option),read(filenames, encoding=None),
                                    read_file(f, source=None),read_string(string, source='<string>'),read_dict(dictionary, source='<dict>'),get(section, option, *, raw=False, vars=None[, fallback])
                                    getint(section, option, *, raw=False, vars=None[, fallback]),getfloat(section, option, *, raw=False, vars=None[, fallback]),getboolean(section, option, *, raw=False, vars=None[, fallback])
                                    items(section, raw=False, vars=None),set(section, option, value),write(fileobject, space_around_delimiters=True),remove_option(section, option),remove_section(section)
>>> config = configparser.ConfigParser()
>>> config['DEFAULT'] = {'ServerAliveInterval': '45',
...                      'Compression': 'yes',
...                      'CompressionLevel': '9'}
>>> config['bitbucket.org'] = {}
>>> config['bitbucket.org']['User'] = 'hg'
>>> config['topsecret.server.com'] = {}
>>> topsecret = config['topsecret.server.com']
>>> topsecret['Port'] = '50022'     # mutates the parser
>>> topsecret['ForwardX11'] = 'no'  # same here
>>> config['DEFAULT']['ForwardX11'] = 'yes'
>>> with open('example.ini', 'w') as configfile:
...   config.write(configfile)

>>> config = configparser.ConfigParser()
>>> config.sections()
[]
>>> config.read('example.ini')
['example.ini']
>>> config.sections()
['bitbucket.org', 'topsecret.server.com']
>>> 'bitbucket.org' in config
True
>>> 'bytebong.com' in config
False
>>> config['bitbucket.org']['User']
'hg'
>>> config['DEFAULT']['Compression']
'yes'
>>> topsecret = config['topsecret.server.com']
>>> topsecret['ForwardX11']
'no'
>>> topsecret['Port']
'50022'
>>> for key in config['bitbucket.org']:  
...     print(key)
user
compressionlevel
serveraliveinterval
compression
forwardx11
>>> config['bitbucket.org']['ForwardX11']
'yes'
config['bitbucket.org'].getboolean('ForwardX11')
config.getboolean('bitbucket.org', 'Compression')

parser.read_dict()
config.read_string(sample_config)

'''


'''
open("myfile.txt", "r", encoding="utf-8")
open("myfile.jpg", "rb")
io.StringIO("some initial text data")
io.BytesIO(b"some initial binary data: \x00\x01")

time:
print(time.gmtime())
print(time.localtime())
print(time.time())
print(time.mktime(time.gmtime()))
print(time.mktime(time.localtime()))
print(time.asctime(time.gmtime()))
print(time.ctime())
time.sleep(1)
#time.strftime()
#time.strptime()
c = time.localtime()
print(c.tm_zone)
print(c.tm_gmtoff)
print(c.tm_hour)

logging :
getpass
platform
print(platform.architecture(),platform.machine(),platform.node(),platform.platform(),platform.processor(),platform.system(),platform.win32_ver())

ctypes:
from ctypes import *
print(windll.kernel32) 
 print(cdll.msvcrt)    
 cdll.LoadLibrary("libc.so.6")  
 libc = CDLL("libc.so.6") 
 windll.kernel32.GetModuleHandleA
getattr(cdll.msvcrt, "??2@YAPAXI@Z") 
cdll.kernel32[1]  
print(libc.time(None)) 
print(hex(windll.kernel32.GetModuleHandleA(None)))  
 GetModuleHandle = windll.kernel32.GetModuleHandleA 
 
'''