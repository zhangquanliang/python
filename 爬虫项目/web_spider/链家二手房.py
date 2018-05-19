# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import re
import requests
from bs4 import BeautifulSoup

url = 'https://sz.lianjia.com/ershoufang/'
response = requests.get(url)
page = re.findall('{"totalPage":(.*?),"curPage":1}', response.text, re.I | re.S)[0]

for i in range(int(page)):
    url = 'https://sz.lianjia.com/ershoufang/pg{}/'.format(i+1)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    house_list = soup.find_all('li', class_='clear')
    for house in house_list:
        title = house.find('div', class_='title').get_text()
        address = house.find('div', class_='address').get_text()
        flood = house.find('div', class_='flood').get_text()
        tag = house.find('div', class_='tag').get_text()
        positionInfo = house.find('div', class_='positionInfo').get_text()
        totalPrice = house.find('div', class_='totalPrice').get_text()
        unitPrice = house.find('div', class_='unitPrice').get_text()
        print(title, address, flood, tag, positionInfo, totalPrice, unitPrice)
    break

        