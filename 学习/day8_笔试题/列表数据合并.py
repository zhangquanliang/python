# -*- coding:utf-8 -*-
"""
author = zhangql
"""

list1 = [2,3,8,4,9,5,6]
list2 = [5,6,10,17,11,2]

list3 = []
for i in list1:
    list3.append(i)
for j in list2:
    list3.append(j)
b = sorted(set(list3))
print(b)
a = ['1', '2', '3', '4', '5', '6']
print(''.join(a))
print(sorted(a))