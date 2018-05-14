# -*- coding:utf-8 -*-
"""
author = zhangql
"""
s = "2121aawdadbaad1213ada"

# 第一种
# for i in s:
#     try:
#         if isinstance(int(i), int):
#             print(i)
#     except:
#         pass

# 第二种
# import re
# a = re.sub('\D', "", s)
# print(a)
