# -*- coding: utf-8 -*-
"""
Title = 在函数内部，可以调用其他函数。如果一个函数在内部调用自身本身，这个函数就是递归函数
Date = 20180410
"""

def age(n):
    if n == 1:
        return 20
    return age(n-1) + 1

print(age(10))
