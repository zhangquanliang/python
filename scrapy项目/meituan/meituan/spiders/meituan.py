# -*- coding: utf-8 -*-
import re
import json
import scrapy
from bs4 import BeautifulSoup


class ExampleSpider(scrapy.Spider):
    name = 'meituan'
    allowed_domains = ['meituan.com']
    start_urls = ['http://hz.meituan.com/s/花甲/']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        page_list = soup.find('nav', class_='mt-pagination').find_all('li', class_='pagination-item num-item')
        result = []
        for i in page_list:
            result.append(int(i.get_text()))
        page = max(result)
        for i in range(page):
            offset = 32 * i
            url = 'http://apimobile.meituan.com/group/v4/poi/pcsearch/50?userid=-1&limit=32&offset={}&cateId=-1&q=%E8%8A%B1%E7%94%B2'.format(offset)
            print(url)
        # for i in lst:
        #     url = 'http:' + i.find('a')['href']
        #     yield scrapy.Request(url, callback=self.parse_html)

    def parse_html(self, response):
        reg = re.findall('"detailInfo":(.*?),"photos":', response.text)
        if len(reg) != 0:
            json_str = json.loads(reg[0])
            name = json_str['name']
            address = json_str['address']
            phone = json_str['phone']
            open_time = json_str['openTime']
            print(name, address, phone, open_time)