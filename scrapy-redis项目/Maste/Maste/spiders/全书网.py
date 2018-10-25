# -*- coding: utf-8 -*-
import scrapy
from ..items import MasteItem
from bs4 import BeautifulSoup
from scrapy_redis.spiders import RedisSpider


class QuanshuSpider(RedisSpider):
    name = 'quanshu'
    # start_urls = ['http://www.quanshuwang.com/']

    redis_key = "novel"

    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(QuanshuSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        novel_type_list = response.xpath('//*[@id="channel-header"]/div/nav/ul//li')
        for novel_type_ in novel_type_list:
            novel_type_url = novel_type_.xpath('a/@href').extract()[0]
            yield scrapy.Request(novel_type_url, callback=self.get_novel_url)

    # 解析类型
    def get_novel_url(self, response):
        novel_url_list = response.xpath('//*[@id="navList"]/section/ul//li')
        for novel_url_ in novel_url_list:
            item = MasteItem()
            novel_url = novel_url_.xpath('span/a[3]/@href').extract()
            item['novel_url'] = novel_url[0]
            print('小说地址', novel_url[0])
            yield item
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            next_url = soup.find('a', class_='next')['href']
            if next_url:
                print('下一页地址', next_url)
                yield scrapy.Request(next_url, callback=self.get_novel_url)
        except:
            return