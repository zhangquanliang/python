# -*- coding:utf-8 -*-
"""
author = zhangql
"""

import chardet

s = '无敌是多么寂寞'.encode('utf8')
a = chardet.detect(s)
print(a)