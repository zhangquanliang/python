# -*- coding: utf-8 -*-
import scrapy
from ..items import SlaverItem
from scrapy_redis.spiders import RedisSpider


class NovelSpider(RedisSpider):
    name = 'novel'
    # allowed_domains = ['novel.com']
    # start_urls = ['https://www.23us.so/xiaoshuo/17458.html']
    redis_key = 'novel_url'

    def parse(self, response):
        author = response.xpath('//*[@id="at"]/tr[1]/td[2]/text()').extract()
        novel_type = response.xpath('//*[@id="at"]/tr[1]/td[1]/a/text()').extract()
        print(author, novel_type)
        item = SlaverItem()
        item['author'] = author[0].replace('\xa0', '')
        item['novel_type'] = novel_type[0]
        return item