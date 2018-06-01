# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import requests
from bs4 import BeautifulSoup
a = requests.get('https://s.1688.com/selloffer/offer_search.htm?keywords=%CA%B5%C4%BE%C6%B4%B0%E5&button_click=top&earseDirect=false&n=y')

soup = BeautifulSoup(a.text, 'html.parser')
# 找到ul标签为fd-clr sm-offer-list得数据
list = soup.find('ul', class_='fd-clr sm-offer-list')
# 在ul标签数据中找到所有li标签得数据，循环
for a in list.find_all('li'):
    try:
        # li标签中得下一个标签为a，class为sm-offer-photoLink sw-dpl-offer-photoLink，取他的title数据
        title = a.find('a', class_='sm-offer-photoLink sw-dpl-offer-photoLink')['title']
    except:
        continue
    # li标签中得下一个标签为span，class为sm-offer-priceNum sw-dpl-offer-priceNum，取他的title数据
    price = a.find('span', class_='sm-offer-priceNum sw-dpl-offer-priceNum')['title']
    # li标签中得下一个标签为div，class为sm-widget-offershopwindowshoprepurchaserate ，取他的文本数据
    huitoulu = a.find('div', class_='sm-widget-offershopwindowshoprepurchaserate ').get_text().strip().replace('\n', '')
    # li标签中得下一个标签为a，class为sm-offer-companyName sw-dpl-offer-companyName sm-offer-name-short，取他的title数据
    # dianpu = a.find('a', class_='sm-offer-companyName sw-dpl-offer-companyName sm-offer-name-short')['title']
    print(title, price, huitoulu)
    print('-' * 100)