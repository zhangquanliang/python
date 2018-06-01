# -*- coding: utf-8 -*-
import re
import os
import scrapy
import pymysql
import requests
from bs4 import BeautifulSoup
count = 0


class ExampleSpider(scrapy.Spider):
    name = 'sumaitong'
    allowed_domains = ['aliexpress.com']
    start_urls = ['https://www.aliexpress.com/category/5090301/mobile-phones.html']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        goods_list = soup.find_all('div', class_='img-container left-block util-clearfix')
        for goods in goods_list:
            goods_url = 'https:' + goods.find('a', class_='picRind')['href']
            yield scrapy.Request(goods_url, callback=self.get_context)
        try:
            next_url = 'https:' + soup.find('div', class_='ui-pagination-navi util-left').find('a', class_='page-next ui-pagination-next')['href']
            print(next_url)
        except:
            return
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)

    def get_context(self, response):
        global count
        count += 1
        url = response.url
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1').get_text()
        try:
            price = soup.find('span', itemprop='lowPrice').get_text().replace(',', '')
        except:
            price = soup.find('span', itemprop='price').get_text().replace(',', '')
        image_url_list = soup.find('ul', class_='image-thumb-list').find_all('li')
        image_url = ""
        for image_url_ in image_url_list:
            image_url += image_url_.find('img')['src'] + "\r\n"
        specifications_list = soup.find('ul', class_='product-property-list util-clearfix').find_all('li')
        specifications = ""
        for specifications_ in specifications_list:
            specifications += specifications_.get_text().replace('\n', '') + "\r\n"
        details_url = re.findall('window.runParams.detailDesc="(.*?)";', response.text, re.I | re.S)
        if len(details_url) == 0:
            return
        else:
            details_url = details_url[0]

        sql = "insert into aliexpress(url, title, price, image_url, specifications, details_url)" \
              " values ('%s', '%s', '%s', '%s', '%s', '%s')" % (url, title, price, image_url, specifications, details_url)
        self.db_insert(sql)

    # 数据库连接入库
    def db_insert(self, sql):
        conn = pymysql.connect(host='localhost', user='root', password='zql9988', database='dianshang',
                               charset='utf8')
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()