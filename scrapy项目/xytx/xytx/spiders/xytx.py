# -*- coding: utf-8 -*-
import scrapy
import pymysql
import requests
import time
import re
pymysql.install_as_MySQLdb()
from bs4 import BeautifulSoup


class XytxSpider(scrapy.Spider):
    name = 'xytx'
    allowed_domains = ["www.zyoo.net"]
    start_urls = ['http://www.zyoo.net/p1.html', 'http://www.zyoo.net/p52.html', 'http://www.zyoo.net/p3.html']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        ul_list = soup.find('ul', id='movie_list').find_all('li')
        for i in ul_list[:10]:
            url = 'http://www.zyoo.net' + i.find('a')['href']
            yield scrapy.Request(url, callback=self.get_qishu)

    # 获取期数
    def get_qishu(self, response):
        reg = re.findall('<a href="(.*?)" title="签证.*?">.*?</a>', response.text)
        if len(reg) == 0:
            reg1 = re.findall('<div class="inner">(.*?)</div>', response.text)
            print('当前查询板块[{}]无签证'.format(reg1[0]))
            return
        url = 'http://www.zyoo.net' + reg[0]
        yield scrapy.Request(url, callback=self.get_qzlb)

    # 获取签证地址列表
    def get_qzlb(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        qzlb_ = soup.find('div', class_='ebook_mulu_list').find_all('li')
        for i in qzlb_:
            url = 'http://www.zyoo.net' + i.find('a')['href']
            yield scrapy.Request(url, callback=self.get_qztp)

    # 获取到签证图片地址
    def get_qztp(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        img_url = soup.find('img', id='oimg', class_='oimg')['src']
        res = requests.get(img_url)
        t = str(time.time() * 1000)
        file = 'images/' + '%s' % t + '.jpg'
        with open(file, 'wb') as f:
            f.write(res.content)