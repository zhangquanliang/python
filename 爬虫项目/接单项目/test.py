# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import random
import time
import requests
from fake_useragent import FakeUserAgent


fk = FakeUserAgent()
for i in range(10):
    try:
        ua = fk.random
        print(ua)
    except:
        print('1111')
        pass