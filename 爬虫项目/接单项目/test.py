# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import requests
import urllib.parse
lista = {'中文': '121', '文章': '123'}
b = urllib.parse.urlencode(lista)
url = 'https://www.baidu.com?{}'.format(b)
print(url)
a = requests.get(url)
print(a.status_code)
print(a.url)