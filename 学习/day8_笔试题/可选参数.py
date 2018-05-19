# -*- coding:utf-8 -*-
"""
author = zhangql
"""


# arpc可选参数, kwarg可选关键字参数
def funcArgsTest(a, b, c=100, *argc, **kwarg):
    sum = a + b + c
    for d in argc:
        sum += d
    for k, v in kwarg.items():
        sum += v
    return sum

print(funcArgsTest(100,200,300,500,600,aa=700,bb=900,cc=1000))