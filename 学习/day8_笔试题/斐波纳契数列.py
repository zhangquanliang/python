# -*- coding:utf-8 -*-
"""
author = zhangql
"""

# 1. 斐波纳契数列
# a, b = 0, 1
# for i in range(1, 13):
#     print('第%s个月：%s对兔子' % (i, b))
#     a, b = b, a + b

# 2. 斐波那契数列
# x = 1
# y = 1
# for i in range(12):
#     print(x)
#     print(y)
#     x = x+y
#     y = x+y


# 3. 斐波那契数列
# def func(num):
#     if num == 1 or num == 2:
#         return 1
#     else:
#         return func(num-2) + func(num-1)
#
#
# for i in range(1, 13):
#     print(func(i))

# 4. 斐波那契数列
# a = 0
# b = 1
# while b < 1000:
#     print(a, b)
#     a, b = b, a+ b

# 5. 斐波那契数列
# lst = []
# for i in range(13):
#     if i == 0 or i == 1:
#         lst.append(1)
#     else:
#         lst.append(lst[i-1] + lst[i-2])
# print(lst)