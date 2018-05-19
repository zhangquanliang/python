# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import urllib3
urllib3.disable_warnings()
import requests
from bs4 import BeautifulSoup


class Diyiwei:
    def __init__(self):
        self.url = 'https://diyiwei.tmall.com/i/asynSearch.htm?_ksTS=1526614242613_377&callback=jsonp378' \
                   '&mid=w-15011940777-0&wid=15011940777&path=/search.htm&search=y&orderType=hotsell_desc&tsearch=y&scene=taobao_shop'
        self.req = requests.session()
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, sdch",
            "accept-language": "zh-CN,zh;q=0.8",
            "cache-control": "max-age=0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
        }

    def get_all_commodity(self):
        res = self.req.get(self.url, headers=self.headers, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        lst = []
        commodity_list = soup.find_all('div', class_='\\"item5line1\\"')
        for commodity_dg in commodity_list:
            commodity_t = commodity_dg.find_all('dl', class_='\\"item')
            for commodity in commodity_t:
                commodity_dict = {}
                name = commodity.find('dd', class_='\\"detail\\"').find('a').get_text().strip()
                price = commodity.find('dd', class_='\\"detail\\"').find('div', class_='\\"attribute\\"').get_text().strip()
                commodity_dict['name'] = name
                commodity_dict['price'] = price
                lst.append(commodity_dict)
        print(len(lst))
        print(lst)


if __name__ == '__main__':
    diyiwei = Diyiwei()
    diyiwei.get_all_commodity()