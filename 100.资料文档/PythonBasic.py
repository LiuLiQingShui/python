


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




'''
You might have noticed that methods like insert, remove or sort that only modify the list have no return value printed – they return the default None. 1 This is a design principle for all mutable data structures in Python
 *-operator to unpack  a list or tuple
**-operator to unpack  a  dictionary or mapping
Note that multiple assignment is really just a combination of tuple packing and sequence unpacking.
'''








