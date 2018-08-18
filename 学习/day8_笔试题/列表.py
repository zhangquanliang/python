# -*- coding:utf-8 -*-
"""
author = zhangql
"""


# def f(x, l=[]):
#     for i in range(x):
#         l.append(i*i)
#     print(l)
#
#
# f(2)
# f(3, [3,2,1])
# f(3)

#
# A0 = dict(zip(('a','b','c','d','e'),(1,2,3,4,5)))
# print(AO)   {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

# 生成器
def func():
    yield '1'

a = func()
for i in a:
    print(i)