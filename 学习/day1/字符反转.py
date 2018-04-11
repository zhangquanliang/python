# -*- coding: utf-8 -*-
s = 'apple'

# 1. 字符串反转
# result = s[::-1]

# 2. 列表反转
# a = list(s)
# a.reverse()
# print("".join(a))

# 3. 递归
# def func(s):
#     if len(s) < 1:
#         return s
#     return func(s[1:]) + s[0]
# reslut = func(s)
# print(reslut)

# 4. 使用栈
# def func(s):
#     l = list(s) #模拟全部入栈
#     result = ""
#     while len(l)>0:
#         result += l.pop() #模拟出栈
#     return result
# result = func(s)
# print(result)