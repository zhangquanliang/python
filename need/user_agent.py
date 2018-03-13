# -*- coding: utf-8 -*-
"""
模拟用户UA
"""
import fake_useragent
ua = fake_useragent.UserAgent()
try:
    while True:
        print(ua.random)
        import time
        time.sleep(1)
except:
    pass