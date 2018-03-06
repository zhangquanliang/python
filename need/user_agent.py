# -*- coding: utf-8 -*-
"""
模拟用户UA
"""
import fake_useragent
ua = fake_useragent.UserAgent()
try:
    for i in range(5):
        print(ua.random)
except:
    pass