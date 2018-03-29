# -*- coding: utf-8 -*-
import urllib.request
"""
urllib.request请求相关
"""
response = urllib.request.urlopen('http://www.baidu.com')
# print(response.read().decode('utf-8'))  # 得到响应数据
# print(response.status)   # 得到响应状态码
print(response.getheaders())   # 得到响应