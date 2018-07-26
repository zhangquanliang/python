# -*- coding:utf-8 -*-
from collections import Counter
a =  [1,2,3,4,5]
print(a[:])
print(a[-2:])
print(sum([x+3 for x in a if x%2==0]))
import datetime

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))