# -*- coding:utf-8 -*-
"""
author = zhangql
"""

# 4. 斐波纳契数列
a, b = 0, 1
for i in range(1, 13):
    print('第%s个月：%s对兔子' % (i, b))
    a, b = b, a + b