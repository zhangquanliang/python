import xlwt
import random
import threadpool
import time
import datetime
import requests
import urllib3
urllib3.disable_warnings()
from selenium import webdriver
url = 'https://xueqiu.com/hq/screener'

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "cache-control": "no-cache",
    "Connection": "keep-alive",
    "Host": "xueqiu.com",
    "Referer": "https://xueqiu.com/hq/screener",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
    "X-Requested-With": "XMLHttpRequest",
    }
response = requests.get(url, headers=headers, verify=True)
cookie_list = response.cookies.get_dict()
cookie = ""
for k, v in cookie_list.items():
    cookie += ';' + k+"="+v
headers_ = headers['cookie'] = cookie

response = requests.get('https://xueqiu.com/stock/screener/screen.json?category=SH&exchange=&areacode=&indcode=&orderby=symbol&order=desc&current=ALL&pct=ALL&page=1&mc=ALL&volume=ALL&_=1524901838913', headers=headers, verify=True)
count = response.json()
print(count['count'])
for mz in count['list']:
    print(mz['name'], mz['volume'])
    print('-' * 100)