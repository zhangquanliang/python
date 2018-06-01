# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy项目.bosszp.bosszp.items import BosszpItem

class ExampleSpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/job_detail/?query=&scity=100010000&industry=&position=']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        job_list_ = soup.find('div', class_='job-list').find('ul').find_all('li')
        for jon_l in job_list_:
            job_url = 'https://www.zhipin.com' + jon_l.find('h3', class_='name').find('a')['href']
            yield scrapy.Request(job_url, callback=self.parse_job)
            # break

    def parse_job(self, response):
        item = BosszpItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        zp_name = soup.find('div', class_='job-detail').find('div', class_='detail-op').find('h2').get_text().strip()
        fr_name = soup.find('div', class_='level-list').find('li').get_text().strip().replace('法人代表：', '')
        # if 1:
        if fr_name == zp_name:
            gsdz = soup.find('div', class_='location-address').get_text().strip()
            date = soup.find('div', class_='job-author').find('span', class_='time').get_text().strip()
        else:
            return
        print(zp_name, gsdz, date)
        item['zp_name'] = zp_name
        item['gsdz'] = gsdz
        item['date'] = date
        yield item