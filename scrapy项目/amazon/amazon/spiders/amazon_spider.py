# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy项目.bosszp.bosszp.items import BosszpItem


class AmazoneSpider(scrapy.Spider):
    name = 'amazon'
    lst = ['B06W5KSDY5', 'B07KNW9466', 'B007OWPQHO', 'B06XZTWJ46']
    allowed_domains = ['amazon.com']

    start_urls = ['https://www.amazon.com/dp/' + i for i in lst]

    def parse(self, response):
        # 获取到当前url, 取商品信息当文件名
        url = response.url
        good_id = str(url).split('dp/')[1]
        f = open(str(good_id) + '.txt', 'a', encoding='utf-8')
        # 取到所有的feature-bullets信息循环
        for item in response.xpath('//*[@id="feature-bullets"]/ul//li'):
            shuju = item.xpath('span[@class="a-list-item"]/text()').extract_first()
            shuju = str(shuju.replace('：', ':')).split(':')[0].replace('\n', '').strip()
            if shuju == '':
                continue
            # 写入到打开的文件中
            f.write(shuju + '\n')
            print(shuju)
            print('-' * 100)
