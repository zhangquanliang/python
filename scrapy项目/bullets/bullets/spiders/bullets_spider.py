# -*- coding: utf-8 -*-
import re
import csv
import scrapy
from bs4 import BeautifulSoup
from ..items import BulletsItem


class BulletsSpider(scrapy.Spider):
    name = 'bullets_spider'
    allowed_domains = ['amazon.com']

    """复制自己的csv文件地址进这里，然后就可以了"""
    reader2 = csv.reader(
        open('/Users/zhangql/python/scrapy项目/bullets/bullets/spiders/asinlist.csv', 'r', encoding='utf_8'))

    start_urls = []
    for i in reader2:
        file_name = str(i[0]).strip()
        goods_t = str(i[-1]).strip()
        url = 'https://www.amazon.com/dp/{}/{}'.format(goods_t, file_name)
        start_urls.append(url)

    def parse(self, response):

        html = response.text
        url = response.url
        month = str(url[-2:]).replace('/', '').replace('\\', '')
        # f = open(file_name, 'a', encoding='utf-8')
        size = str(html).count('fbExpandableSection')
        if size > 3:
            reslist = response.xpath('//*[@id="fbExpandableSectionContent"]//ul//li')
        else:
            reslist = response.xpath('//*[@id="feature-bullets"]/ul//li')
        text = ''
        bullestitem = BulletsItem()
        # 取到所有的feature-bullets信息循环
        for item in reslist:
            shuju = item.xpath('span[@class="a-list-item"]/text()').extract_first()
            shuju = str(shuju.replace('\n', '')).strip()
            if shuju == '':
                continue
            # 写入到打开的文件中
            # f.write(shuju)
            text += shuju + ' '
            print(shuju)
            print('-' * 100)
        if text == '':
            return
        bullestitem['month'] = month
        bullestitem['text'] = text
        yield bullestitem
